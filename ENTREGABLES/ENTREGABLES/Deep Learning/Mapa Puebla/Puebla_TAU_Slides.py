from manim import *
from manim import config
import numpy as np
import torch, torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from PIL import Image
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, to_rgba
from matplotlib.tri import Triangulation
import colorsys
import math
config.disable_caching = True

config.background_color = "#0b0b0b"
config.pixel_width, config.pixel_height, config.frame_rate = 1920, 1080, 60
config.tex_template.add_to_preamble(r"\usepackage{amsmath}")
Text.set_default(font_size=36)
Tex.set_default(font_size=36)
MathTex.set_default(font_size=36)


ORIGINAL_IMG   = "/home/gustavo/SS/verde_transparente.png"
OUT_1_IMG      = "/home/gustavo/SS/1_neurona.png"
OUT_32_IMG     = "/home/gustavo/SS/32_neuronas.png"
OUT_1000_IMG   = "/home/gustavo/SS/1000_neuronas.png"
OUT_40000_IMG  = "/home/gustavo/SS/40000_neuronas.png"

MAP_PATH   = "/home/gustavo/SS/100k.png"
TITLE_TEXT = "Asi para un mayor número de neuronas se obtiene:"
TIME = 3.2
BEIGE, WHITE = "#e6dcc7", "#ffffff"
NODE_COLOR   = BLUE
LINE_COLOR   = PINK
PANEL_COLOR  = WHITE
W_NODE, W_LINE, W_BOX = 3.0, 3.0, 3.0
R = 0.16


MOSAIC_TILE_H      = 3.6
MOSAIC_GAP_X       = 1.4
MOSAIC_CAPTION_GAP = 0.35
MOSAIC_ARROW_GAP   = 0.18
MOSAIC_ARROW_W     = 12
MOSAIC_ARROW_TIP   = 0.40

def _mosaic_palette_hsv(n):
    hs = np.linspace(0, 1, n, endpoint=False)
    rgb = [colorsys.hsv_to_rgb(h, 0.65, 1.0) for h in hs]
    return (np.array(rgb)*255).astype(np.uint8)

def _mosaic_edge_rgba_from_labels(labels, thickness=2, color=(255,255,255,200)):
    H, W = labels.shape
    edge = np.zeros((H, W), dtype=np.uint8)
    edge[:, 1:] |= (labels[:, 1:] != labels[:, :-1])
    edge[1:, :] |= (labels[1:, :] != labels[:-1, :])
    for _ in range(max(0, thickness-1)):
        e = edge
        up    = np.pad(e[1:, :],  ((1,0),(0,0)))
        down  = np.pad(e[:-1, :], ((0,1),(0,0)))
        left  = np.pad(e[:, 1:],  ((0,0),(1,0)))
        right = np.pad(e[:, :-1], ((0,0),(0,1)))
        edge = np.maximum.reduce([e, up, down, left, right])
    rgba = np.zeros((H, W, 4), dtype=np.uint8)
    rgba[edge>0] = color
    return rgba

def mosaic_max_affine_torch(n_planes=8, res=420, seed=0, device="cpu"):
    torch.manual_seed(seed)
    A = torch.randn(n_planes, 2, device=device)
    b = torch.empty(n_planes, device=device).uniform_(-0.8, 0.8)
    xs = torch.linspace(-1, 1, res, device=device)
    ys = torch.linspace(-1, 1, res, device=device)
    XX, YY = torch.meshgrid(xs, ys, indexing="xy")
    grid = torch.stack([XX.reshape(-1), YY.reshape(-1)], dim=1)
    with torch.no_grad():
        labels = (grid @ A.T + b).argmax(dim=1).reshape(res, res).cpu().numpy()
    img = _mosaic_palette_hsv(n_planes)[labels]
    edges = _mosaic_edge_rgba_from_labels(labels, thickness=2)
    return img, edges

def arrow_between_m(left_mob, right_mob):
    start = left_mob.get_right() + RIGHT*MOSAIC_ARROW_GAP
    end   = right_mob.get_left() + LEFT*MOSAIC_ARROW_GAP
    return Arrow(start, end, buff=0, stroke_width=MOSAIC_ARROW_W, color=WHITE,
                 max_tip_length_to_length_ratio=0.20, tip_length=MOSAIC_ARROW_TIP).set_z_index(10)

def stack_mosaic(img_rgb, edges_rgba, height=MOSAIC_TILE_H):
    base  = ImageMobject(img_rgb).set_height(height)
    over  = ImageMobject(edges_rgba).set_height(height).move_to(base).set_z_index(5)
    return Group(base, over)


def set_bicubic(im: ImageMobject):
    try:
        from PIL import Image as PILImage
        try: im.set_resampling_algorithm(PILImage.Resampling.BICUBIC)
        except: im.set_resampling_algorithm(PILImage.BICUBIC)
    except: pass

def safe_image(path: str, max_h=4.6, max_w=4.8):
    try:
        im = ImageMobject(path)
        im.set_z_index(1)
        im.scale_to_fit_height(max_h)
        if im.width > max_w:
            im.scale_to_fit_width(max_w)
        return im
    except Exception:
        box = RoundedRectangle(width=max_w, height=max_h, corner_radius=0.15,
                               stroke_color=RED, fill_opacity=0.05)
        txt = Text("Imagen no encontrada", font_size=28).move_to(box.get_center())
        return Group(box, txt)

def column_with_caption(content: Mobject, caption: str):
    cap = Tex(caption, font_size=26).set_color(WHITE)
    return Group(content, cap).arrange(DOWN, buff=0.60)

def mask_by_color(img_rgb, color_rgb, tol=30):
    diff = (img_rgb.astype(np.int16) - np.array(color_rgb, dtype=np.int16))
    dist2 = (diff**2).sum(axis=-1)
    return dist2 < (tol * tol)

def to_norm_coords(xs, ys, W, H):
    xs = xs.astype(np.float32); ys = ys.astype(np.float32)
    x_norm = xs/(W/2.0) - 1.0
    y_norm = (H - ys)/(H/2.0) - 1.0
    return np.stack([x_norm, y_norm], axis=1)

def coords_from_mask(mask, W, H):
    ys, xs = np.where(mask)
    if len(xs) == 0: return np.empty((0,2), dtype=np.float32)
    return to_norm_coords(xs, ys, W, H)

class PueblaNet(nn.Module):
    def __init__(self, hidden_layers=[64,64,64]):
        super().__init__()
        layers = [nn.Linear(2, hidden_layers[0]), nn.ReLU()]
        for i in range(len(hidden_layers)-1):
            layers += [nn.Linear(hidden_layers[i], hidden_layers[i+1]), nn.ReLU()]
        layers += [nn.Linear(hidden_layers[-1], 2)]
        self.model = nn.Sequential(*layers)
    def forward(self, x): return self.model(x)

def train_and_make_assets(img_path, out_dir="assets_puebla",
                          hidden=[64,64,64], epochs=40, bs=256, lr=5e-3,
                          grid_res=180, puebla_color=(200,50,50), tol=35):
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(img_path).convert("RGB").resize((600, 600))
    img_np = np.array(img); H, W = img_np.shape[:2]
    puebla_mask = mask_by_color(img_np, puebla_color, tol=tol)
    gray = img_np.mean(axis=2); dark_lines = gray < 40
    not_puebla_mask = (~puebla_mask) & (~dark_lines)
    p_coords = coords_from_mask(puebla_mask, W, H)
    o_coords = coords_from_mask(not_puebla_mask, W, H)
    n_per_class = int(min(2000, len(p_coords), len(o_coords)))
    if n_per_class < 500:
        puebla_mask = mask_by_color(img_np, puebla_color, tol=max(tol, 50))
        not_puebla_mask = (~puebla_mask) & (~dark_lines)
        p_coords = coords_from_mask(puebla_mask, W, H)
        o_coords = coords_from_mask(not_puebla_mask, W, H)
        n_per_class = int(min(2000, len(p_coords), len(o_coords)))
        if n_per_class == 0:
            raise RuntimeError("No se pudo detectar Puebla con el color/tolerancia dados.")
    rng = np.random.default_rng(42)
    p_idx = rng.choice(len(p_coords), n_per_class, replace=False)
    o_idx = rng.choice(len(o_coords), n_per_class, replace=False)
    X = np.vstack([o_coords[o_idx], p_coords[p_idx]]).astype(np.float32)
    y = np.concatenate([np.zeros(n_per_class), np.ones(n_per_class)]).astype(np.int64)
    ds = TensorDataset(torch.from_numpy(X), torch.from_numpy(y))
    dl = DataLoader(ds, batch_size=bs, shuffle=True)
    torch.manual_seed(0)
    model = PueblaNet(hidden_layers=hidden)
    criterion = nn.CrossEntropyLoss()
    optimz = optim.Adam(model.parameters(), lr=lr)
    model.train()
    for _ in range(epochs):
        for xb, yb in dl:
            loss = criterion(model(xb), yb)
            optimz.zero_grad(); loss.backward(); optimz.step()
    xs = np.linspace(-1, 1, grid_res)
    ys = np.linspace(-1, 1, grid_res)
    XX, YY = np.meshgrid(xs, ys)
    grid = np.stack([XX, YY], axis=-1).reshape(-1, 2).astype(np.float32)
    with torch.no_grad():
        logits_all = model(torch.from_numpy(grid))
        probs = torch.softmax(logits_all, dim=1)[:, 1].numpy()
        logits = logits_all.numpy()
        g_flat = logits[:,1] - logits[:,0]
    P = probs.reshape(grid_res, grid_res)
    g = g_flat.reshape(grid_res, grid_res)
    labels = (P >= 0.5).astype(np.int32)
    mask_small = np.array(
        Image.fromarray((puebla_mask*255).astype(np.uint8)).resize(
            (grid_res, grid_res), resample=Image.NEAREST)
    ) > 127
    def save_layer_winners(layer_idx, filename):
        with torch.no_grad():
            x = torch.from_numpy(grid)
            lin_id = 0; winners = None
            for m in model.model:
                if isinstance(m, nn.Linear):
                    z = x @ m.weight.T + m.bias
                    if lin_id == layer_idx:
                        winners = torch.argmax(z, dim=1).numpy().reshape(grid_res, grid_res)
                        break
                    x = torch.relu(z); lin_id += 1
            if winners is None:
                raise ValueError("El modelo no tiene suficientes capas lineales.")
        K = int(winners.max()) + 1
        cmap = plt.cm.gist_ncar(np.linspace(0, 1, max(K, 32)))
        fig, ax = plt.subplots(figsize=(4,4), facecolor="black")
        ax.imshow(winners, origin="lower", extent=[-1,1,-1,1], cmap=ListedColormap(cmap))
        ax.contour(mask_small.astype(float), levels=[0.5], colors=["magenta"], linewidths=1.8,
                   origin="lower", extent=[-1,1,-1,1])
        ax.set_xticks([]); ax.set_yticks([]); ax.set_frame_on(False)
        fig.subplots_adjust(0,0,1,1)
        fig.savefig(out_dir/filename, dpi=280, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
    save_layer_winners(0, "layer1.png")
    save_layer_winners(1, "layer2.png")
    save_layer_winners(2, "layer3.png")
    fig, ax = plt.subplots(figsize=(4,4), facecolor="black")
    ax.imshow(img_np, extent=[-1,1,1,-1])
    class_cmap = ListedColormap(["#127a8a", "#d28a00"])
    ax.imshow(np.flipud(labels), alpha=0.45, extent=[-1,1,1,-1], cmap=class_cmap)
    ax.contour(P, levels=[0.5], colors=["magenta"], linewidths=2.2,
               origin="upper", extent=[-1,1,-1,1])
    ax.contour(mask_small.astype(float), levels=[0.5], colors=["#ffd54f"], linewidths=1.2,
               origin="lower", extent=[-1,1,-1,1])
    ax.set_xticks([]); ax.set_yticks([]); ax.set_frame_on(False)
    fig.subplots_adjust(0,0,1,1)
    fig.savefig(out_dir/"decision.png", dpi=300, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    x_flat = XX.flatten()
    y_flat = YY.flatten()
    y_flat_top = -y_flat
    tri_top = Triangulation(x_flat, y_flat_top)
    tri_mean = g.flatten()[tri_top.triangles].mean(axis=1)
    c_pos = to_rgba("#127a8a", 0.9); c_neg = to_rgba("#d28a00", 0.9)
    facecols = np.where(tri_mean[:,None] >= 0, c_pos, c_neg)
    s = max(np.percentile(np.abs(g), 95), 1.0)
    z_vals = np.clip(g.flatten(), -s, s)
    fig = plt.figure(figsize=(6.0, 4.5), facecolor="black")
    ax = fig.add_subplot(111, projection='3d', facecolor="black")
    surf = ax.plot_trisurf(tri_top, z_vals, linewidth=0.35, edgecolor=(1,1,1,0.12),
                           antialiased=False)
    surf.set_facecolors(facecols)
    ax.contour(XX, -YY, g, levels=[0.0], zdir='z', offset=0.0, colors=["magenta"], linewidths=2.2)
    ax.contour(XX, YY, mask_small.astype(float), levels=[0.5], zdir='z', offset=-s, colors=["#ffd54f"], linewidths=1.2)
    ax.view_init(elev=26, azim=-55)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-s, s)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_box_aspect([1,1,0.6])
    ax.grid(False)
    fig.subplots_adjust(0,0,1,1)
    fig.savefig(out_dir/"surface3d.png", dpi=300, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    return {k: out_dir/k for k in ["layer1.png","layer2.png","layer3.png","decision.png","surface3d.png"]}

def scale_to_fit(mobj, max_w, max_h):
    sx = max_w / mobj.width
    sy = max_h / mobj.height
    mobj.scale(min(sx, sy))
    return mobj

def tile_with_label(img_path, label_text, label_h=0.35, font_size=26):
    img = ImageMobject(str(img_path))
    bar = Rectangle(width=img.width, height=label_h, fill_opacity=0.95,
                    fill_color=BLACK, stroke_width=0).next_to(img, UP, buff=0)
    txt = Text(label_text, font_size=font_size, color=WHITE).move_to(bar.get_center())
    frame = Rectangle(width=img.width, height=img.height+label_h,
                      stroke_width=0, fill_opacity=0).move_to(img.get_center() + UP*label_h/2)
    return Group(frame, img, bar, txt)


class PerceptronWidget(VGroup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        r = 0.18
        x_node = Circle(r, BLUE).set_fill(BLUE, 0.1).move_to(LEFT*2.6 + UP*0.7)
        w_node = Circle(r, BLUE).set_fill(BLUE, 0.1).move_to(LEFT*2.6 + DOWN*0.7)
        h_node = Circle(r, YELLOW).set_fill(YELLOW, 0.1).move_to(RIGHT*0.0)
        o_node = Circle(r, GREEN).set_fill(GREEN, 0.1).move_to(RIGHT*2.6)
        x_lbl = MathTex("x", font_size=28).move_to(x_node.get_center())
        w_lbl = MathTex("w", font_size=28).move_to(w_node.get_center())
        h_lbl = MathTex("h", font_size=28).move_to(h_node.get_center())
        o_lbl = MathTex(r"\hat{y}", font_size=28).move_to(o_node.get_center())
        e1 = Arrow(x_node.get_right(), h_node.get_left(), buff=0.06, stroke_width=2)
        e2 = Arrow(w_node.get_right(), h_node.get_left(), buff=0.06, stroke_width=2)
        e3 = Arrow(h_node.get_right(), o_node.get_left(), buff=0.06, stroke_width=2)
        self.nodes = VGroup(x_node, w_node, h_node, o_node)
        self.labels = VGroup(x_lbl, w_lbl, h_lbl, o_lbl)
        self.edges  = VGroup(e1, e2, e3)
        self.hidden_nodes = VGroup(h_node)
        self.highlight_target = self.hidden_nodes
        self.extra_bottom_text = "Regresion lineal"
        self.add(self.edges, self.nodes, self.labels)
    def play_animation(self, scene: Scene):
        scene.play(LaggedStart(*[FadeIn(n, scale=0.8) for n in self.nodes], lag_ratio=0.15))
        scene.play(LaggedStart(*[Create(e) for e in self.edges], lag_ratio=0.2))
        scene.play(LaggedStart(*[FadeIn(l) for l in self.labels], lag_ratio=0.1))
        scene.play(LaggedStartMap(Indicate, self.nodes, scale_factor=1.15))

class HiddenLayerWidget(VGroup):
    def __init__(self, cols=4, rows=8, total_neurons=32, **kwargs):
        super().__init__(**kwargs)
        r = 0.12
        x_node = Circle(r, BLUE).set_fill(BLUE, 0.1).move_to(LEFT*3.0 + UP*0.6)
        w_node = Circle(r, BLUE).set_fill(BLUE, 0.1).move_to(LEFT*3.0 + DOWN*0.6)
        o_node = Circle(r, GREEN).set_fill(GREEN, 0.1).move_to(RIGHT*3.0)
        hidden_nodes = VGroup()
        xs = np.linspace(-0.7, 0.7, max(2, int(cols)))
        ys = np.linspace( 1.5,-1.5, max(2, int(rows)))
        for yy in ys:
            for xx in xs:
                node = Circle(r, YELLOW).set_fill(YELLOW, 0.1).move_to(np.array([xx, yy, 0]))
                hidden_nodes.add(node)
        x_lbl = MathTex("x", font_size=24).move_to(x_node.get_center())
        w_lbl = MathTex("w", font_size=24).move_to(w_node.get_center())
        o_lbl = MathTex(r"\hat{y}", font_size=24).move_to(o_node.get_center())
        edges = VGroup()
        for node in hidden_nodes:
            edges.add(Line(x_node.get_right(), node.get_left(),  stroke_width=1.6))
            edges.add(Line(w_node.get_right(), node.get_left(),  stroke_width=1.6))
            edges.add(Line(node.get_right(),  o_node.get_left(), stroke_width=1.6))
        self.all_nodes = VGroup(x_node, w_node, *hidden_nodes, o_node)
        self.labels    = VGroup(x_lbl, w_lbl, o_lbl)
        self.edges     = edges
        self.hidden_nodes = hidden_nodes
        self.highlight_target = hidden_nodes
        self.add(self.edges, self.all_nodes, self.labels)
    def play_animation(self, scene: Scene):
        scene.play(LaggedStart(*[FadeIn(n, scale=0.85) for n in self.all_nodes], lag_ratio=0.05))
        scene.play(LaggedStart(*[Create(e) for e in self.edges], lag_ratio=0.01))
        scene.play(FadeIn(self.labels))
        scene.play(LaggedStartMap(Flash, self.all_nodes, flash_radius=0.25))

class LargeHiddenLayerWidget(VGroup):
    def __init__(self, total_neurons=1000, cols=12, rows=10, **kwargs):
        super().__init__(**kwargs)
        self.cols = max(6, int(cols))
        self.rows = max(6, int(rows))
        r = 0.10
        x_node = Circle(r, BLUE).set_fill(BLUE, 0.1).move_to(LEFT*3.0 + UP*0.6)
        w_node = Circle(r, BLUE).set_fill(BLUE, 0.1).move_to(LEFT*3.0 + DOWN*0.6)
        o_node = Circle(r, GREEN).set_fill(GREEN, 0.1).move_to(RIGHT*3.0)
        x_lbl = MathTex("x", font_size=24).move_to(x_node.get_center())
        w_lbl = MathTex("w", font_size=24).move_to(w_node.get_center())
        o_lbl = MathTex(r"\hat{y}", font_size=24).move_to(o_node.get_center())
        hidden_nodes = VGroup()
        xs = np.linspace(-0.9, 0.9, self.cols)
        ys = np.linspace( 1.4,-1.4, self.rows)
        for yy in ys:
            for xx in xs:
                node = Circle(r, YELLOW).set_fill(YELLOW, 0.1).move_to(np.array([xx, yy, 0]))
                hidden_nodes.add(node)
        edges = VGroup()
        n_sample = min(26, len(hidden_nodes))
        idxs = np.linspace(0, len(hidden_nodes)-1, n_sample, dtype=int) if n_sample > 0 else []
        for k in idxs:
            node = hidden_nodes[k]
            edges.add(Line(x_node.get_right(), node.get_left(),  stroke_width=1.2))
            edges.add(Line(w_node.get_right(), node.get_left(),  stroke_width=1.2))
            edges.add(Line(node.get_right(),  o_node.get_left(), stroke_width=1.2))
        self.all_nodes = VGroup(x_node, w_node, *hidden_nodes, o_node)
        self.labels    = VGroup(x_lbl, w_lbl, o_lbl)
        self.edges     = edges
        self.hidden_nodes = hidden_nodes
        self.highlight_target = hidden_nodes
        self.add(self.edges, self.all_nodes, self.labels)
    def play_animation(self, scene: Scene):
        scene.play(LaggedStart(*[FadeIn(m, scale=0.85) for m in self.all_nodes], lag_ratio=0.02))
        scene.play(LaggedStart(*[Create(e) for e in self.edges], lag_ratio=0.01))
        scene.play(FadeIn(self.labels))
        scene.play(LaggedStartMap(Flash, self.all_nodes, flash_radius=0.22))


WRITE_SPEED = 5

class UnifiedScene(Scene):
    def play(self, *anims, **kwargs):
        if "run_time" not in kwargs:
            kwargs["run_time"] = WRITE_SPEED
        return super().play(*anims, **kwargs)
    def slide_cut(self, clear=True):
        if not clear:
            return
        if self.mobjects:
            g = Group(*self.mobjects)
            self.play(FadeOut(g), rate_func=linear)



S47_WRITE_SPEED = 5
S47_CURVE_DRAW_TIME = 3.0
S47_CURVE_COLOR = GREEN_E
S47_GRAPH_W = 6.6
S47_GRAPH_H = 3.2
S47_LOSS_BLOCK_SHIFT_UP = 0.25*UP

S47_LOSS_SERIES = {
    1: [(1,0.7314),(2,0.6970),(3,0.6691),(4,0.6491),(5,0.6324),
        (6,0.6172),(7,0.6055),(8,0.5971),(9,0.5901),(10,0.5841)],
    32: [(1,0.6537),(2,0.6104),(3,0.5573),(4,0.4899),(5,0.4218),
         (6,0.3619),(7,0.3209),(8,0.2956),(9,0.2797),(10,0.2694),
         (11,0.2636),(12,0.2566),(13,0.2531),(14,0.2473),(15,0.2466),
         (16,0.2427),(17,0.2388),(18,0.2353),(19,0.2347),(20,0.2328)],
    1000: [(1,0.5052),(2,0.3075),(3,0.2532),(4,0.2246),(5,0.2037),
           (6,0.1901),(7,0.1853),(8,0.1812),(9,0.1785),(10,0.1696),
           (11,0.1662),(12,0.1677),(13,0.1748),(14,0.1652),(15,0.1606),
           (16,0.1653),(17,0.1628),(18,0.1557),(19,0.1555),(20,0.1533),
           (21,0.1516),(22,0.1535),(23,0.1484),(24,0.1491),(25,0.1542),
           (26,0.1524),(27,0.1499),(28,0.1482),(29,0.1481),(30,0.1481)],
    40000: [(1,3.1458),(2,1.3089),(3,0.7849),(4,0.4501),(5,0.3187),
            (6,0.2381),(7,0.2359),(8,0.1983),(9,0.2586),(10,0.2506),
            (11,0.2998),(12,0.3886),(13,0.3798),(14,0.3022),(15,0.2040),
            (16,0.1584),(17,0.1859),(18,0.2895),(19,0.2635),(20,0.2694),
            (21,0.1547),(22,0.1842),(23,0.2092),(24,0.1612),(25,0.1432),
            (26,0.1796),(27,0.2085),(28,0.2041),(29,0.2413),(30,0.2183),
            (31,0.1664),(32,0.1596),(33,0.3984),(34,0.3597),(35,0.1898),
            (36,0.1672),(37,0.1766),(38,0.1365),(39,0.1547),(40,0.1808),
            (41,0.2007),(42,0.2150),(43,0.1769),(44,0.1281),(45,0.1483),
            (46,0.1486),(47,0.1295),(48,0.1252),(49,0.1670),(50,0.1480)]
}

def S47_x_ticks(max_epoch: int):
    if max_epoch == 10:
        return list(range(0, 11, 2))
    ticks = list(range(0, max_epoch + 1, 10))
    if ticks[-1] != max_epoch:
        ticks.append(max_epoch)
    return ticks

def S47_y_ticks_nice(ys, max_labels=4):
    y_min, y_max = float(min(ys)), float(max(ys))
    if y_min == y_max:
        return [round(y_min, 3)]
    pad = 0.02 * (y_max - y_min + 1e-9)
    a, b = y_min - pad, y_max + pad
    rng = b - a
    candidates = [0.02, 0.05, 0.1, 0.2, 0.25, 0.5, 1.0]
    step = min([s for s in candidates if rng / s <= (max_labels - 1)] or [candidates[-1]])
    y0 = math.floor(a / step) * step
    y1 = math.ceil(b / step) * step
    vals, v = [], y0
    while v <= y1 + 1e-9:
        vals.append(round(v, 3))
        v += step
    while len(vals) > max_labels:
        vals = vals[::2]
    return vals

def S47_build_loss_axes(series, force_y_count: int | None = None):
    xs = [e for e, _ in series]
    ys = [l for _, l in series]
    max_epoch = xs[-1]
    x_ticks = S47_x_ticks(max_epoch)

    if force_y_count is not None and force_y_count >= 2:
        ymax_raw = max(ys)
        y_min = 0.0
        y_max = float(math.ceil(ymax_raw + 1e-9))
        step = (y_max - y_min) / (force_y_count - 1)
        y_ticks = [round(y_min + i * step, 3) for i in range(force_y_count)]
    else:
        y_ticks = S47_y_ticks_nice(ys, max_labels=4)
        y_min, y_max = min(y_ticks), max(y_ticks)
        step = (y_ticks[1] - y_ticks[0]) if len(y_ticks) >= 2 else 1.0

    x_len = S47_GRAPH_W
    y_len = S47_GRAPH_H

    x_min, x_max = 0, max_epoch
    x_step = x_ticks[1] - x_ticks[0] if len(x_ticks) >= 2 else max_epoch

    axes = Axes(
        x_range=[x_min, x_max, x_step],
        y_range=[y_min, y_max, step],
        x_length=x_len, y_length=y_len,
        tips=False,
        axis_config={"color": WHITE, "stroke_width": 2, "include_numbers": False}
    )

    x_labels = VGroup(*[
        MathTex(str(t), font_size=13, color=WHITE).move_to(
            axes.c2p(t, y_min) + DOWN * 0.30
        ) for t in x_ticks
    ])
    y_labels = VGroup(*[
        MathTex(f"{t:.3f}", font_size=13, color=WHITE).move_to(
            axes.c2p(x_min, t) + LEFT * 0.30
        ) for t in y_ticks
    ])

    xlabel = Text("Épocas", font_size=16, color=WHITE).next_to(axes.x_axis, DOWN, buff=0.30)
    ylabel = Text("Pérdida", font_size=16, color=WHITE).rotate(90*DEGREES).next_to(axes.y_axis, LEFT, buff=0.30)

    graph = axes.plot_line_graph(
        xs, ys, add_vertex_dots=False, line_color=S47_CURVE_COLOR, stroke_width=4
    ).set_z_index(7)

    axes_group = VGroup(axes, x_labels, y_labels, xlabel, ylabel).set_z_index(6)
    return axes_group, graph

def S47_sample_map_boundary_points(image_path: str, left_img: Mobject, n_points: int):
    arr = np.array(Image.open(image_path).convert("RGBA"))
    H, W = arr.shape[:2]
    alpha = arr[..., 3] > 10

    up    = np.pad(alpha, ((1,0),(0,0)), constant_values=False)[:-1, :]
    down  = np.pad(alpha, ((0,1),(0,0)), constant_values=False)[1:,  :]
    left  = np.pad(alpha, ((0,0),(1,0)), constant_values=False)[:, :-1]
    right = np.pad(alpha, ((0,0),(0,1)), constant_values=False)[:,  1:]
    boundary = alpha & (~up | ~down | ~left | ~right)

    ys, xs = np.nonzero(boundary)
    if len(xs) == 0:
        return []
    idx = np.random.choice(len(xs), size=min(n_points, len(xs)), replace=False)
    xs, ys = xs[idx], ys[idx]

    x_left = left_img.get_corner(DL)[0]
    y_top  = left_img.get_corner(UL)[1]
    w_m    = left_img.width
    h_m    = left_img.height

    pts = []
    for xpx, ypx in zip(xs, ys):
        xm = x_left + ((xpx + 0.5) / W) * w_m
        ym = y_top  - ((ypx + 0.5) / H) * h_m
        pts.append(np.array([xm, ym, 0.0]))
    return pts

def S47_build_edge_pixels_flow_from_map(left_img: Mobject, ins_nodes: VGroup,
                                        n_dots: int = 56, dot_size: float = 0.045,
                                        run_time_each: float = 0.8, lag_ratio: float = 0.07,
                                        image_path: str = ORIGINAL_IMG):
    starts = S47_sample_map_boundary_points(image_path, left_img, n_dots)
    dots = VGroup()
    anims = []
    target_x = ins_nodes[0].get_center()
    target_y = ins_nodes[1].get_center()

    for k, start in enumerate(starts):
        target = target_x if (k % 2 == 0) else target_y
        d = Dot(start, radius=dot_size, color=WHITE, stroke_width=0)
        dots.add(d)
        path = Line(start, target)
        anims.append(Succession(
            MoveAlongPath(d, path, rate_func=linear, run_time=run_time_each),
            FadeOut(d, run_time=0.15)
        ))

    flow = LaggedStart(*anims, lag_ratio=lag_ratio)
    return dots, flow


def make_row_s47(left: Mobject, center_placeholder: Mobject, right: Mobject, title: str):
    title_m = Tex(title, font_size=42).set_color(WHITE).to_edge(UP)
    left_col   = column_with_caption(left,   "Original")
    center_col = Group(center_placeholder)  
    right_col  = column_with_caption(right,  "Salida")
    row = Group(left_col, center_col, right_col).arrange(RIGHT, buff=0.7)
    max_w = config.frame_width - 0.6
    if row.width > max_w:
        row.scale_to_fit_width(max_w)
    row.next_to(title_m, DOWN, buff=0.5)
    container = Group(title_m, row)
    max_h = config.frame_height - 0.4
    if container.height > max_h:
        container.scale_to_fit_height(max_h)
    return container, row


def s47_edge_between(a: Mobject, b: Mobject,
                     r_a: float = R, r_b: float = R,
                     color=LINE_COLOR, width=W_LINE):
    """Línea recortada para tocar tangencialmente los nodos circulares."""
    pa = a.get_center(); pb = b.get_center()
    v = pb - pa
    n = np.linalg.norm(v)
    if n < 1e-6:
        return Line(pa, pb, stroke_color=color, stroke_width=width).set_z_index(10)
    vhat = v / n
    start = pa + vhat * r_a     
    end   = pb - vhat * r_b     
    return Line(start, end,
                stroke_color=color, stroke_width=width, stroke_opacity=0.96
           ).set_z_index(10)

def build_panel_net_s47(anchor: Mobject, qty_text: str, mode_center: str):
    C = anchor.get_center()
    p_w, p_h = 2.10, 4.20
    panel = RoundedRectangle(width=p_w, height=p_h, corner_radius=0.22,
                             stroke_color=PANEL_COLOR, stroke_width=W_BOX).move_to(C)

    x8, x2 = -0.30, 0.64
    Y2_SPACING = 0.90
    y2 = [+Y2_SPACING/2, -Y2_SPACING/2]
    STEP = Y2_SPACING / 2.0
    DOTS_Y = (+0.25, 0.00, -0.25)
    DOT_MARGIN = R + 0.12
    first_top = DOTS_Y[0] + DOT_MARGIN
    y_top = [first_top + i*STEP for i in range(4)]
    y_bot = [-y for y in y_top[::-1]]
    y8_list = y_top + y_bot

    x_in = x8 - 0.50

    def mk_nodes(x_local, ys):
        vg = VGroup()
        for y in ys:
            n = Circle(radius=R, color=NODE_COLOR, stroke_width=W_NODE).set_fill(NODE_COLOR, 1.0)
            n.move_to(panel.get_center() + np.array([x_local, y, 0]))
            n.set_z_index(40)
            vg.add(n)
        return vg

    ins  = mk_nodes(x_in, y2)
    ins_labels = VGroup(
        MathTex(r"\mathbf{x}", font_size=24, color=BLACK).move_to(ins[0].get_center()).set_z_index(50),
        MathTex(r"\mathbf{y}", font_size=24, color=BLACK).move_to(ins[1].get_center()).set_z_index(50),
    )

    central = mk_nodes(x8, [0.0]) if mode_center == "single" else mk_nodes(x8, y8_list)
    outs = mk_nodes(x2, y2)

    edges_in, edges_out = VGroup(), VGroup()
    for a in ins:
        for b in central:
            edges_in.add(s47_edge_between(a, b))     

    for b in central:
        for q in outs:
            edges_out.add(s47_edge_between(b, q))    


    strip = Rectangle(width=0.26, height=(abs(DOTS_Y[0]) + abs(DOTS_Y[2])) + 0.70,
                      stroke_width=0, fill_color=config.background_color, fill_opacity=1.0
    ).move_to(panel.get_center() + np.array([x8, 0.0, 0])).set_z_index(20)

    DOT_R = 0.045
    vdots = VGroup(
        Dot(panel.get_center() + np.array([x8, DOTS_Y[0], 0]), radius=DOT_R, color=WHITE, stroke_width=0),
        Dot(panel.get_center() + np.array([x8, DOTS_Y[1], 0]), radius=DOT_R, color=WHITE, stroke_width=0),
        Dot(panel.get_center() + np.array([x8, DOTS_Y[2], 0]), radius=DOT_R, color=WHITE, stroke_width=0),
    ).set_z_index(99)
    if mode_center == "single":
        vdots = VGroup()

    brace = BraceBetweenPoints(panel.get_corner(DL) + LEFT*0.14,
                               panel.get_corner(UL) + LEFT*0.14,
                               direction=LEFT, color=BEIGE).set_stroke(color=BEIGE, width=W_BOX)
    qty = Text(qty_text, font_size=24, color=BEIGE).rotate(90*DEGREES)
    qty.next_to(brace, LEFT, buff=0.06).set_y(panel.get_center()[1]).set_z_index(100)

    return panel, ins, ins_labels, central, outs, edges_in, edges_out, strip, vdots, brace, qty



def animate_like_slide8_s47(scene: Scene, title_m, row, qty_text: str, mode_center: str):
    left_col, center_col, right_col = row[0], row[1], row[2]
    left_img = left_col[0]
    center_anchor = center_col[0]

    def splay(*anims, rt=None):
        return scene.play(*anims, run_time=(S47_WRITE_SPEED if rt is None else rt))

    splay(FadeIn(title_m, shift=UP))
    splay(FadeIn(left_col, shift=LEFT*0.3))
    splay(FadeIn(center_col, shift=UP*0.2))

    panel, ins, ins_labels, central, outs, edges_in, edges_out, strip, vdots, brace, qty = \
        build_panel_net_s47(center_anchor, qty_text, mode_center)

    dots, flow_anim = S47_build_edge_pixels_flow_from_map(
        left_img, ins, n_dots=56, dot_size=0.042, run_time_each=0.80, lag_ratio=0.07,
        image_path=ORIGINAL_IMG
    )
    scene.add(dots)
    splay(
        AnimationGroup(
            LaggedStart(*[FadeIn(n, scale=0.6) for n in ins], lag_ratio=0.10),
            FadeIn(ins_labels),
            flow_anim,
            lag_ratio=0.0
        )
    )

    splay(LaggedStart(*[FadeIn(n, scale=0.6) for n in central], lag_ratio=0.05))
    splay(LaggedStart(*[Create(e) for e in edges_in], lag_ratio=0.0015))
    splay(Create(panel))
    if len(vdots) > 0:
        splay(FadeIn(strip))
        splay(FadeIn(vdots))
    splay(Create(brace), FadeIn(qty))
    splay(FadeOut(VGroup(panel, brace, qty, strip)))  

    splay(LaggedStart(*[FadeIn(n, scale=0.6) for n in outs], lag_ratio=0.10))

    net_group = VGroup(ins, ins_labels, central, outs, edges_in, vdots)
    splay(FadeOut(title_m))
    SCALE_DOWN = 0.82
    SHIFT_UP   = 1.35*UP
    splay(net_group.animate.scale(SCALE_DOWN).move_to(center_anchor.get_center() + SHIFT_UP))

    n_neurons = int(qty_text)
    series = S47_LOSS_SERIES[n_neurons]

    if n_neurons == 40000:
        axes_group, graph = S47_build_loss_axes(series, force_y_count=4)
    else:
        axes_group, graph = S47_build_loss_axes(series)

    loss_block = VGroup(axes_group, graph)
    loss_block.next_to(net_group, DOWN, buff=0.28)
    loss_block.shift(S47_LOSS_BLOCK_SHIFT_UP)

    splay(FadeIn(axes_group, shift=DOWN*0.12))
    scene.play(Create(graph), run_time=S47_CURVE_DRAW_TIME)

    splay(FadeOut(loss_block))
    splay(net_group.animate.scale(1.0/SCALE_DOWN).move_to(center_anchor.get_center()))

    splay(LaggedStart(*[Create(e) for e in edges_out], lag_ratio=0.0015))

    right_img = right_col[0]
    y_arrow = 0.5*(outs[0].get_center()[1] + outs[1].get_center()[1])
    start_x = outs.get_right()[0] + 0.20
    end_x   = right_img.get_left()[0] - 0.10
    start = np.array([start_x, y_arrow, 0.0])
    end   = np.array([end_x,   y_arrow, 0.0])

    arrow = Line(start, end, color=WHITE, stroke_width=4.0).add_tip(tip_length=0.20)
    splay(Create(arrow))
    splay(FadeIn(right_col, shift=RIGHT*0.25))
    scene.wait(0.4)


class AproximacionUniversal(UnifiedScene):
    
    # ======= SLIDE 1 ===========
    def slide_1(self):
        write_speed = 3.2
        t0 = Tex("Aproximación mediante Redes neuronales", font_size=52)
        t0.set_color_by_tex("Aproximación mediante Redes neuronales", BLUE)
        self.play(Write(t0, run_time=write_speed)); self.wait(0.8); self.play(FadeOut(t0))
        texto = Tex(
            r"\textbf{Teorema de Aproximación Universal}\\",
            r"\vskip 12pt",
            r"Una red neuronal con al menos una capa oculta, ",
            r"y un número suficiente de neuronas, ",
            r"puede aproximar cualquier función continua ",
            r"definida en un intervalo compacto, ",
            r"con la precisión deseada.",
            font_size=26
        )
        texto.set_color_by_tex("Teorema de Aproximación Universal", BLUE)
        texto.to_edge(UP)
        self.play(Write(texto, run_time=write_speed))
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1.05, 0.25],
            x_length=9.2, y_length=4.0,
            axis_config={"color": WHITE, "include_numbers": True, "font_size": 28},
        )
        labels = axes.get_axis_labels(x_label=MathTex("x"), y_label=MathTex("y"))
        VGroup(axes, labels).next_to(texto, DOWN, buff=0.7)
        def f_target(x):
            return 0.5 + 0.5*(0.75*np.sin(x) + 0.25*np.cos(3*x))
        target_graph = axes.plot(lambda x: f_target(x), color=RED, stroke_width=4)
        self.play(Create(axes), Write(labels))
        self.play(Create(target_graph))
        sigmoid = lambda z: 1.0/(1.0 + np.exp(-z))
        N = 16
        centers = np.linspace(-2.8, 2.8, N)
        width = 3.8
        ws_fixed = np.full(N, width)
        bs_fixed = -ws_fixed * centers
        xs_fit = np.linspace(-3.0, 3.0, 801)
        Phi = np.column_stack([np.ones_like(xs_fit)] + [sigmoid(ws_fixed[j]*xs_fit + bs_fixed[j]) for j in range(N)])
        y_fit = f_target(xs_fit)
        coef, *_ = np.linalg.lstsq(Phi, y_fit, rcond=None)
        c0_star = float(coef[0]); a_star  = coef[1:].astype(float)
        c0 = ValueTracker(0.0)
        al = [ValueTracker(0.0) for _ in range(N)]
        def nn_sum(x):
            s = c0.get_value()
            for j in range(N):
                s += al[j].get_value() * sigmoid(ws_fixed[j]*x + bs_fixed[j])
            return np.clip(s, 0.0, 1.05)
        nn_graph = always_redraw(lambda: axes.plot(lambda x: nn_sum(x), color=GREEN, stroke_width=4))
        self.play(Create(nn_graph))
        self.play(c0.animate.set_value(c0_star))
        half = N//2
        self.play(*[al[j].animate.set_value(a_star[j]) for j in range(half)], rate_func=smooth)
        self.play(*[al[j].animate.set_value(a_star[j]) for j in range(half, N)], rate_func=smooth)
        self.wait(0.8)

    
    # ======= SLIDE 2 ===========
    def slide_2(self):
        titulo = Tex(r"de manera formal:", font_size=22, color=WHITE)
        l1 = Tex(r"Sea $\varphi:\mathbb{R}\to\mathbb{R}$ una activación continua, acotada y no constante.",
                 tex_environment="flushleft", font_size=22, color=WHITE)
        eq = MathTex(r"F(x) = \sum_{j=1}^{N} \, \alpha_j\, \varphi(w_j^{\mathsf T}x + \theta_j)", font_size=22)
        eq.set_color_by_tex("F(x)", BLUE); eq.set_color_by_tex(r"\varphi", GREEN)
        l2 = Tex(r"con $\alpha_j\in\mathbb{R}$, $w_j\in\mathbb{R}^n$, $\theta_j\in\mathbb{R}$.",
                 tex_environment="flushleft", font_size=24, color=WHITE)
        l3 = Tex(r"Entonces, el conjunto de tales $F$ es \textbf{denso} en $C([0,1]^n)$.",
                 tex_environment="flushleft", font_size=22, color=WHITE)
        concl1 = Tex(r"Equivalente: para toda $f\in C([0,1]^n)$ y todo $\varepsilon>0$,",
                     tex_environment="flushleft", font_size=22, color=WHITE)
        concl2 = MathTex(
            r"\exists\, N,\{\alpha_j,w_j,\theta_j\}_{j=1}^{N}\ \text{tal que}\ "
            r"\sup_{x\in[0,1]^n}\big|f(x)-F(x)\big|<\varepsilon.",
            font_size=22, color=WHITE
        )
        grupo = VGroup(titulo, l1, eq, l2, l3, concl1, concl2).arrange(DOWN, buff=0.28)
        grupo.scale_to_fit_height(config.frame_height * 0.9)
        if grupo.width > config.frame_width * 0.94: grupo.set_width(config.frame_width * 0.94)
        grupo.move_to(ORIGIN)
        self.play(Write(titulo))
        self.play(Write(l1))
        self.play(Write(eq))
        self.play(Write(l2))
        self.play(Write(l3))
        self.play(Write(concl1))
        self.play(Write(concl2))
        self.wait(1.0)

    
    # ======= SLIDE 2.1 ===========
    def slide_2_1(self):
        t = Tex(
            r"Para visualizar el Teorema de Aproximación Universal, consideramos la tarea de aproximar un contorno "
            r"(mapa de Puebla) a partir de coordenadas $(x,y)$.\\[8pt]"
            r"Con PyTorch (biblioteca de Deep Learning en Python) entrenamos un \textbf{MLP} (Multi-Layer Perceptron) que, "
            r"usando s\'olo $(x,y)$, ajusta la frontera del mapa.\\[8pt]"
            r"La calidad de la aproximaci\'on mejora al aumentar la capacidad del modelo (m\'as neuronas y/o capas).",
            font_size=30, color=WHITE
        )
        if t.width > config.frame_width*0.92:
            t.scale_to_fit_width(config.frame_width*0.92)
        if t.height > config.frame_height*0.85:
            t.scale_to_fit_height(config.frame_height*0.85)
        t.move_to(ORIGIN)
        self.play(Write(t))
        self.wait(0.6)

    
    # ======= SLIDE 2.2 ===========
    def slide_2_2(self):
        p1 = Tex(
            r"El teorema establece, de manera t\'ecnica, que una red con una capa oculta y activaci\'on no polin\'omica "
            r"(p.\,ej., ReLU) puede aproximar arbitrariamente bien cualquier funci\'on continua en un conjunto compacto.",
            font_size=26, color=WHITE
        )
        eq = MathTex(
            r"(x,y)\ \mapsto\ \underbrace{\text{Linear}\ \xrightarrow{\ \mathrm{ReLU}\ }\ \cdots\ \xrightarrow{\ \mathrm{ReLU}\ }\ \text{Linear}}_{\text{MLP con }k\text{ capas ocultas}}\ "
            r"\to\ \text{2 salidas (logits)}",
            font_size=26, color=WHITE
        )
        p2 = Tex(
            r"Los \textbf{logits} son las puntuaciones que la red asigna a ``dentro'' y ``fuera''. "
            r"El contorno es la l\'inea donde esas puntuaciones empatan; el entrenamiento mueve esa l\'inea hasta pegarla al borde real, "
            r"y m\'as neuronas la hacen m\'as flexible y precisa para calcar la forma.",
            font_size=30, color=WHITE
        )
        g = VGroup(p1, eq, p2).arrange(DOWN, buff=0.5)
        g.scale_to_fit_height(config.frame_height*0.88)
        if g.width > config.frame_width*0.94: g.set_width(config.frame_width*0.94)
        g.move_to(ORIGIN)
        self.play(Write(p1))
        self.play(Write(eq))
        self.play(Write(p2))
        self.wait(0.6)

    # ======= SLIDE 2.3 ===========
    def slide_2_3(self):
        
        t_intro = Tex(
            r"Durante el entrenamiento, una \textit{época} es un recorrido completo por el conjunto de ejemplos."
            r" En cada recorrido, el modelo procesa los datos en mini-lotes, calcula su \textbf{pérdida}"
            r" y ajusta los \textbf{pesos} mediante retropropagación, con la intención de que en la siguiente pasada cometa menos error.",
            font_size=26, color=WHITE
        ).scale_to_fit_width(config.frame_width*0.86).to_edge(UP, buff=0.8)

        formula = MathTex(
            r"\mathcal{L}\;=\;-\frac{1}{N}\sum_{i=1}^{N}\Big[\,y_i\log p_i\;+\;(1-y_i)\log(1-p_i)\,\Big]",
            color="#74b6ff", font_size=36
        )
        formula.next_to(t_intro, DOWN, buff=0.6)

        
        self.play(Write(t_intro))
        self.play(Write(formula))

        
        
        formula_final = formula.copy()
        mapa_dummy = ImageMobject(ORIGINAL_IMG).scale_to_fit_height(3.0)  

        
        top_layout = Group(mapa_dummy, formula_final).arrange(RIGHT, aligned_edge=UP, buff=1.0)
        top_layout.to_edge(UP, buff=0.9)

        
        target_formula_center = formula_final.get_center()
        target_mapa_center    = mapa_dummy.get_center()

        
        self.play(FadeOut(t_intro))
        self.play(formula.animate.move_to(target_formula_center))

        
        mapa = ImageMobject(ORIGINAL_IMG).scale_to_fit_height(3.0)
        mapa.move_to(target_mapa_center)
        self.play(FadeIn(mapa))

        
        top_grp_final = Group(mapa, formula)  
        t_final = Tex(
            r"En nuestro ejercicio del mapa de Puebla, $y_i\in\{0,1\}$ indica si el punto cae dentro (1) o fuera (0) de la silueta verde,"
            r" y $p_i$ es la probabilidad que la red asigna a “estar dentro de Puebla”."
            r" A medida que avanzan las épocas, la \textbf{pérdida} tiende a descender y, con más neuronas, baja más rápido,"
            r" aunque pueden aparecer pequeñas oscilaciones por la optimización y el muestreo por mini-lotes.",
            font_size=26, color=WHITE
        ).scale_to_fit_width(config.frame_width*0.92)

        t_final.next_to(top_grp_final, DOWN, buff=0.7)
        
        if t_final.get_bottom()[1] < -config.frame_height/2 + 0.35:
            t_final.to_edge(DOWN, buff=0.55)

        self.play(Write(t_final))

        
        self.play(FadeOut(Group(top_grp_final, t_final), run_time=4))

    
    # ======= SLIDE 3 ===========
    def slide_3(self):
        self.camera.background_color = BLACK

        img_path = "/home/gustavo/Downloads/mapaPuebla.png"
        assets = train_and_make_assets(img_path)

        title = Text("Aprendizaje por capas y frontera de decisión", font_size=22, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))

        g1 = tile_with_label(assets["layer1.png"], "Layer 1")
        g2 = tile_with_label(assets["layer2.png"], "Layer 2")
        g3 = tile_with_label(assets["layer3.png"], "Layer 3")
        g4 = tile_with_label(assets["decision.png"], "Frontera de Decisión")

        def _mirror_h(mobj: Mobject):
            c = mobj.get_center()
            mobj.apply_matrix(np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float))
            mobj.move_to(c)
        for tile in (g1, g2, g3):
            if len(tile.submobjects) >= 2:
                _mirror_h(tile.submobjects[1])

        row_gap, col_gap = 0.45, 0.35
        row1 = Group(g1, g2).arrange(RIGHT, buff=col_gap)
        row2 = Group(g3, g4).arrange(RIGHT, buff=col_gap)
        left_grid = Group(row1, row2).arrange(DOWN, buff=row_gap)

        surf = ImageMobject(str(assets["surface3d.png"]))
        set_bicubic(surf)

        FW, FH = config.frame_width, config.frame_height
        side_margin, gap_lr = 0.5, 0.5
        left_w = FW * 0.56
        right_w = FW - left_w - 2*side_margin - gap_lr
        top_margin = 0.4
        avail_h = FH - (title.height + 2*top_margin)
        left_h = right_h = avail_h

        scale_to_fit(left_grid, left_w, left_h)
        scale_to_fit(surf, right_w, right_h)

        y_center = -FH/2 + avail_h/2
        left_center  = np.array([-FW/2 + side_margin + left_w/2,  y_center, 0])
        right_center = np.array([ FW/2 - side_margin - right_w/2, y_center, 0])

        left_grid.move_to(left_center)
        surf.move_to(right_center)

        tiles = [g1, g2, g3, g4]
        self.play(LaggedStart(*[FadeIn(t, shift=UP*0.25) for t in tiles], lag_ratio=0.3))
        self.play(FadeIn(surf, shift=RIGHT*0.25))
        self.wait(1.0)

        all_objs = Group(title, left_grid, surf)
        self.play(FadeOut(all_objs, rate_func=linear))
        self.remove(all_objs)
        self.wait(0.2)

    
    # ======= SLIDE 4 ===========
    def slide_4(self):
        left_img  = safe_image(ORIGINAL_IMG)
        right_img = safe_image(OUT_1_IMG)
        center_ph = Rectangle(width=5.8, height=4.4, stroke_width=0, fill_opacity=0)
        container, row = make_row_s47(left_img, center_ph, right_img, "Aproximación con 1 neurona")
        title_m = container.submobjects[0]
        animate_like_slide8_s47(self, title_m, row, qty_text="1", mode_center="single")
        self.slide_cut()

    
    # ======= SLIDE 5 ===========
    def slide_5(self):
        left_img  = safe_image(ORIGINAL_IMG)
        right_img_32 = safe_image(OUT_32_IMG)
        center_ph = Rectangle(width=5.8, height=4.4, stroke_width=0, fill_opacity=0)
        container, row = make_row_s47(left_img, center_ph, right_img_32, "Aproximación con 32 neuronas")
        title_m = container.submobjects[0]
        animate_like_slide8_s47(self, title_m, row, qty_text="32", mode_center="block8")
        self.slide_cut()

    
    # ======= SLIDE 6 ===========
    def slide_6(self):
        left_img  = safe_image(ORIGINAL_IMG)
        right_img_1000 = safe_image("/home/gustavo/SS/1000_neuronas.png")
        center_ph = Rectangle(width=5.8, height=4.4, stroke_width=0, fill_opacity=0)
        container, row = make_row_s47(left_img, center_ph, right_img_1000, "Aproximación con 1000 neuronas")
        title_m = container.submobjects[0]
        animate_like_slide8_s47(self, title_m, row, qty_text="1000", mode_center="block8")
        self.slide_cut()

    
    # ======= SLIDE 7 ===========
    def slide_7(self):
        left_img  = safe_image(ORIGINAL_IMG)
        right_img_40000 = safe_image("/home/gustavo/SS/40000_neuronas.png")
        center_ph = Rectangle(width=5.8, height=4.4, stroke_width=0, fill_opacity=0)
        container, row = make_row_s47(left_img, center_ph, right_img_40000, "Aproximación con 40000 neuronas")
        title_m = container.submobjects[0]
        animate_like_slide8_s47(self, title_m, row, qty_text="40000", mode_center="block8")
        self.slide_cut()

    
    # ======= SLIDE 7.1 ===========
    def slide_7_1(self):
        l1 = "Geométricamente, las ReLU construyen una función a trozos lineales: cada neurona aporta un corte;"
        l2 = "miles de cortes forman un mosaico poligonal que se ciñe a la silueta de Puebla."
        caption = Paragraph(l1, l2, alignment="center", line_spacing=0.55)
        caption.set_width(config.frame_width - 1.2)
        (img1, e1) = mosaic_max_affine_torch(n_planes=8,   res=420, seed=11)
        (img2, e2) = mosaic_max_affine_torch(n_planes=64,  res=420, seed=12)
        (img3, e3) = mosaic_max_affine_torch(n_planes=256, res=420, seed=13)
        g1 = stack_mosaic(img1, e1)
        g2 = stack_mosaic(img2, e2)
        g3 = stack_mosaic(img3, e3)
        fila_mosaicos = Group(g1, g2, g3).arrange(RIGHT, buff=MOSAIC_GAP_X)
        a12 = arrow_between_m(g1, g2)
        a23 = arrow_between_m(g2, g3)
        fila = Group(g1, a12, g2, a23, g3)
        columna = Group(caption, fila).arrange(DOWN, buff=MOSAIC_CAPTION_GAP)
        if columna.width > config.frame_width*0.94:
            columna.scale_to_fit_width(config.frame_width*0.94)
        if columna.height > config.frame_height*0.9:
            columna.scale_to_fit_height(config.frame_height*0.9)
        columna.move_to(ORIGIN)
        self.play(Write(caption))
        self.play(FadeIn(g1, shift=DOWN))
        self.play(GrowArrow(a12))
        self.play(FadeIn(g2, shift=DOWN))
        self.play(GrowArrow(a23))
        self.play(FadeIn(g3, shift=DOWN))
        self.wait(0.6)

    
    # ======= SLIDE 8 ===========
    def slide_8(self):
        title = Text(TITLE_TEXT, color=BEIGE, font_size=26, weight="SEMIBOLD").to_edge(UP, buff=0.85)
        self.play(Write(title, run_time=1.0*TIME))
        p_w, p_h = 2.10, 4.20
        panel = RoundedRectangle(width=p_w, height=p_h, corner_radius=0.22,
                                 stroke_color=PANEL_COLOR, stroke_width=W_BOX)
        x8, x2 = -0.30, 0.64
        Y2_SPACING = 0.90
        y2 = [+Y2_SPACING/2, -Y2_SPACING/2]
        STEP = Y2_SPACING / 2.0
        DOTS_Y = (+0.25, 0.00, -0.25)
        DOT_MARGIN = R + 0.12
        first_top = DOTS_Y[0] + DOT_MARGIN
        y_top = [first_top + i*STEP for i in range(4)]
        y_bot = [-y for y in y_top[::-1]]
        y8 = y_top + y_bot
        def mk_nodes(x, ys):
            vg = VGroup()
            for y in ys:
                n = Circle(radius=R, color=NODE_COLOR, stroke_width=W_NODE).set_fill(NODE_COLOR, opacity=1.0)
                n.move_to(panel.get_center() + np.array([x, y, 0])); n.set_z_index(40); vg.add(n)
            return vg
        col8 = mk_nodes(x8, y8)
        col2 = mk_nodes(x2, y2)
        strip = Rectangle(width=0.26, height=(abs(DOTS_Y[0]) + abs(DOTS_Y[2])) + 0.70,
                          stroke_width=0, fill_color=config.background_color, fill_opacity=1.0
        ).move_to(panel.get_center() + np.array([x8, 0.0, 0])).set_z_index(20)
        edges = VGroup()
        for a in col8:
            for b in col2:
                e = Line(a.get_center(), b.get_center(),
                         stroke_color=LINE_COLOR, stroke_width=W_LINE, stroke_opacity=0.96)
                e.set_z_index(10); edges.add(e)
        DOT_R = 0.045
        vdots = VGroup(
            Dot(panel.get_center() + np.array([x8, DOTS_Y[0], 0]), radius=DOT_R, color=WHITE, stroke_width=0),
            Dot(panel.get_center() + np.array([x8, DOTS_Y[1], 0]), radius=DOT_R, color=WHITE, stroke_width=0),
            Dot(panel.get_center() + np.array([x8, DOTS_Y[2], 0]), radius=DOT_R, color=WHITE, stroke_width=0),
        ).set_z_index(99)
        brace = BraceBetweenPoints(panel.get_corner(DL) + LEFT*0.14,
                                   panel.get_corner(UL) + LEFT*0.14,
                                   direction=LEFT, color=BEIGE).set_stroke(color=BEIGE, width=W_BOX)
        qty = Text("100,000", font_size=24, color=BEIGE).rotate(90*DEGREES)
        qty.next_to(brace, LEFT, buff=0.06).set_y(panel.get_center()[1]).set_z_index(100)
        VGroup(panel, edges, strip, col8, col2, vdots, brace, qty).scale(0.98).to_edge(LEFT, buff=1.95)
        self.play(Create(panel, run_time=0.55*TIME))
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in col8], lag_ratio=0.05, run_time=0.60*TIME))
        self.play(LaggedStart(*[FadeIn(n, scale=0.6) for n in col2], lag_ratio=0.10, run_time=0.40*TIME))
        self.play(LaggedStart(*[Create(e) for e in edges], lag_ratio=0.0015, run_time=0.80*TIME))
        self.play(FadeIn(strip, run_time=0.20*TIME))
        self.play(FadeIn(vdots, run_time=0.25*TIME))
        self.play(Create(brace, run_time=0.40*TIME), FadeIn(qty, run_time=0.35*TIME))
        frame_size = 4.55
        img = ImageMobject(MAP_PATH); set_bicubic(img)
        img.set_height(frame_size * 0.828)
        img.set_z_index(2)
        img.to_edge(RIGHT, buff=1.95).shift(UP*0.01)
        arrow = Arrow(start=panel.get_right() + RIGHT*0.20,
                      end=img.get_left() + LEFT*0.10,
                      stroke_color=WHITE, stroke_width=4.0, tip_length=0.20)
        self.play(Create(arrow, run_time=0.55*TIME))
        self.play(FadeIn(img, shift=RIGHT*0.06, run_time=0.60*TIME))
        self.wait(2.6*TIME)

    
    # ======= SLIDE 9 ===========
    def slide_9(self):
        txt = Tex(
            r"A medida que aumentamos el número de neuronas, la red neuronal se vuelve capaz de reproducir formas cada vez mas complejas. "
            r"Lo que comenzó con una frontera lineal termina aproximando con aguda precisión el contorno real del mapa.\\[8pt]"
            r"Este teorema trasciende la clasificación de mapas, se aplica en la reconstrucción de señales, la modelación de sistemas físicos, "
            r"la simulación de procesos biológicos, el análisis de imágenes médicas, predicción de modelos dinámicos financieros y en general, "
            r"en modelos matemáticos complejos",
            font_size=34, color=WHITE
        )
        if txt.width > config.frame_width*0.92:
            txt.scale_to_fit_width(config.frame_width*0.92)
        if txt.height > config.frame_height*0.85:
            txt.scale_to_fit_height(config.frame_height*0.85)
        txt.move_to(ORIGIN)
        self.play(Write(txt, run_time=3.2))
        self.wait(0.4)
        self.play(FadeOut(txt, run_time=3.2))

    
    def make_row(self, left: Mobject, center: Mobject, right: Mobject, title: str):
        title_m = Tex(title, font_size=42).set_color(WHITE).to_edge(UP)
        left_col   = column_with_caption(left,   "Original")
        center_col = column_with_caption(center, "Representación de la red")
        right_col  = column_with_caption(right,  "Salida")
        row = Group(left_col, center_col, right_col).arrange(RIGHT, buff=0.7)
        max_w = config.frame_width - 0.6
        if row.width > max_w:
            row.scale_to_fit_width(max_w)
        row.next_to(title_m, DOWN, buff=0.5)
        container = Group(title_m, row)
        max_h = config.frame_height - 0.4
        if container.height > max_h:
            container.scale_to_fit_height(max_h)
        return container, center

    def show_slide(self, container: Group, center_obj: Mobject, net_size_text: str, animate_center: callable, hold=1.0):
        title_m, row = container.submobjects
        self.play(FadeIn(title_m, shift=UP))
        self.play(FadeIn(row[0], shift=LEFT*0.3))
        self.play(FadeIn(row[1], shift=UP*0.2))
        self.play(FadeIn(row[2], shift=RIGHT*0.3))
        animate_center(center_obj)
        if hasattr(center_obj, "extra_bottom_text"):
            t = center_obj.extra_bottom_text
            bottom_label = Tex(t, font_size=32).next_to(center_obj.highlight_target, DOWN, buff=0.2)
            self.play(FadeIn(bottom_label))
        else:
            bottom_label = VGroup()
        target = getattr(center_obj, "highlight_target", center_obj)
        box = SurroundingRectangle(target, color=RED, buff=0.18, stroke_width=6)
        self.play(Create(box))
        label = Tex(net_size_text, font_size=34, color=RED).next_to(target, UP, buff=0.15)
        self.play(FadeTransform(box, label))
        self.wait(hold)
        self.play(FadeOut(Group(container, label, bottom_label)), rate_func=linear)

    def construct(self):
        self.slide_1(); self.slide_cut()
        self.slide_2(); self.slide_cut()
        self.slide_2_1(); self.slide_cut()
        self.slide_2_2(); self.slide_cut()
        self.slide_2_3(); self.slide_cut()
        self.slide_4(); self.slide_cut()
        self.slide_5(); self.slide_cut()
        self.slide_6(); self.slide_cut()
        self.slide_7(); self.slide_cut()
        self.slide_7_1(); self.slide_cut()
        self.slide_3(); self.slide_cut()
        self.slide_8(); self.slide_cut()
        self.slide_9(); self.slide_cut()


# manim -pql Puebla_TAU.py AproximacionUniversal --disable_caching

