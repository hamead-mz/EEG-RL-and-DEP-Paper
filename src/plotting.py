import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from scipy.interpolate import griddata

from src.spectral import wavelet_transform
from configuration.local import directories

def movmean(A, k):

    win_length = k
    MAFA = []
    
    if len(A) < k:

        print("I don't know how to calculate this, The window must be less than length. So the length forced to be len(A)")

        win_length = len(A)

    new_elements_len = len(A) - win_length + 1

    for element in range(new_elements_len):

        MAFA.append(np.mean(A[element : (element + 1) + k ]))

    return np.array(MAFA)

def random_block_sampling(Length: int, NumBlock: int, NumSample_inBlock: int):

    Block_Len = int(Length / NumBlock)

    if  NumSample_inBlock >= Block_Len:

        NumSample_inBlock = Block_Len

    SampleMat = []

    for Block in range(NumBlock - 1):

        SampleMat.append(np.random.permutation(Block_Len)[:NumSample_inBlock] + Block * Block_Len)

    SampleMat.append(Length - 1 - np.random.permutation(Block_Len)[:NumSample_inBlock])

    return np.array(SampleMat)

def determined_block_sampling(Length: int, NumBlock: int, NumSample_inBlock: int):

    Block_Len = int(Length / NumBlock)

    # assert NumSample_inBlock <= Block_Len, 'Number of Samples in Blocks must be less than length of Block'

    if  NumSample_inBlock >= Block_Len:

        NumSample_inBlock = Block_Len

    SampleMat = []

    for Block in range(NumBlock - 1):

        SampleMat.append(np.int32(np.arange(NumSample_inBlock)) + Block * Block_Len)

    SampleMat.append(Length - 1 - np.int32(np.arange(NumSample_inBlock)))

    return np.array(SampleMat)

def wavelet_freqs_ret(spectral_res = 50):

    shData = np.sin(2 * np.pi * np.linspace(0, 1, 500))
    _, freqs = wavelet_transform(shData, return_freqs = True, Spectral_Res = spectral_res)
    freqs = freqs[::-1]

    return freqs

def load_coords():

    FCoords = np.load(directories['ch_coords_dir'], allow_pickle =True).item()

    ValidChannels = [key for key in FCoords.keys()]
    CoordMat = np.array([FCoords[ValidChannel] for ValidChannel in ValidChannels])

    return ValidChannels, CoordMat

def confidence_bounds_generator(data, confidence_level = 1.96):

    assert data.ndim < 3 and data.ndim > 0, "Data must be vector or 2 way matrix"

    if data.ndim == 2:

        y_Upper = []
        y_Lower = []

        [num_samples, num_timePoint] = data.shape

        for t_p in range(num_timePoint):

            U_tmp, L_tmp = confidence_bound(data[:, t_p], confidence_level)

            y_Upper.append(L_tmp)
            y_Lower.append(U_tmp)

        return np.array(y_Upper), np.array(y_Lower)
    
    else:

        return 0
    
def confidence_bound(data, confidence_level):

    return np.mean(data) + confidence_level * np.std(data) / np.sqrt(len(data)), np.mean(data) - confidence_level * np.std(data) / np.sqrt(len(data))

def plot_scalp_topography( # AI-assisted #
    ax,
    ch_xy,
    ch_values,
    vmin=None,
    vmax=None,
    cmap="viridis",
    show_colorbar=False,
    n_grid=200,
    head_radius=0.5,
    nose=True,
    ears=True,
    shading="gouraud",
    contour=False,          # False | True | "lines" | "filled" | "both"
    n_levels=10,
    contour_color="k",
    contour_linewidth=0.6,
):
    """
    Plot EEG scalp topography inside a circular head outline.
    Returns: ax, im, cbar
    """
    # ---------- sanitize
    ch_xy = np.asarray(ch_xy, dtype=float)
    ch_values = np.asarray(ch_values, dtype=float)
    if ch_xy.ndim != 2 or ch_xy.shape[1] != 2:
        raise ValueError("ch_xy must be of shape (n_channels, 2)")
    if ch_values.ndim != 1 or ch_values.shape[0] != ch_xy.shape[0]:
        raise ValueError("ch_values must be of shape (n_channels,) and match ch_xy length")

    # ---------- color limits
    if vmin is None or vmax is None:
        finite_vals = ch_values[np.isfinite(ch_values)]
        if vmin is None:
            vmin = np.nanmin(finite_vals) if finite_vals.size else 0.0
        if vmax is None:
            vmax = np.nanmax(finite_vals) if finite_vals.size else 1.0
        if vmin == vmax:
            vmin, vmax = vmin - 1e-9, vmax + 1e-9

    # ---------- grid
    r = float(head_radius)
    x = np.linspace(-r, r, int(n_grid))
    y = np.linspace(-r, r, int(n_grid))
    X, Y = np.meshgrid(x, y)

    # ---------- interpolate (linear + nearest fill)
    Zi_lin = griddata(points=ch_xy, values=ch_values, xi=(X, Y), method="linear")
    Zi_nn  = griddata(points=ch_xy, values=ch_values, xi=(X, Y), method="nearest")
    Zi     = np.where(np.isnan(Zi_lin), Zi_nn, Zi_lin)

    # ---------- mask circle
    mask = (X**2 + Y**2) <= (r**2)
    Zi_masked = np.ma.array(Zi, mask=~mask)

    # ---------- cmap with transparent 'bad'
    cmap_obj = plt.get_cmap(cmap) if isinstance(cmap, str) else cmap
    try:
        cmap_obj = cmap_obj.copy()
    except Exception:
        from copy import copy as _copy
        cmap_obj = _copy(cmap_obj)
    cmap_obj.set_bad(alpha=0.0)

    im = ax.imshow(
        Zi_masked,
        extent=(-r, r, -r, r),
        origin="lower",
        interpolation="bicubic",
        cmap=cmap_obj,
        vmin=vmin,
        vmax=vmax,
        aspect="equal",
        zorder=1,
    )

    # ---------- contours
    if isinstance(contour, bool):
        contour_mode = "both" if contour else "none"
    elif contour is None:
        contour_mode = "none"
    else:
        contour_mode = str(contour).lower()

    cf = None
    if contour_mode != "none":
        levels = np.linspace(vmin, vmax, int(n_levels))
        if contour_mode in ("filled", "both"):
            cf = ax.contourf(
                X, Y, Zi_masked, levels=levels, cmap=cmap_obj,
                antialiased=False, zorder=2
            )
        if contour_mode in ("lines", "both"):
            ax.contour(
                X, Y, Zi_masked, levels=levels, colors=contour_color,
                linewidths=float(contour_linewidth), zorder=3
            )

    # ---------- head outline
    head = Circle((0, 0), r, edgecolor="k", facecolor="none", linewidth=1.5, zorder=5)
    ax.add_patch(head)

    if nose:
        nose_w = 0.08 * r
        nose_h = 0.14 * r
        nose_y = r
        nose_pts = np.array([[0.0, nose_y + nose_h], [-nose_w, nose_y], [nose_w, nose_y]])
        ax.add_patch(Polygon(nose_pts, closed=True, edgecolor="k", facecolor="k", linewidth=1.0, zorder=6))

    if ears:
        ear_w = 0.04 * r
        ear_h = 0.14 * r
        ear_y0 = 0.0
        ax.add_patch(Polygon([[-r, ear_y0 - ear_h], [-r - ear_w, ear_y0], [-r, ear_y0 + ear_h]],
                             closed=False, edgecolor="k", linewidth=1.2, zorder=6))
        ax.add_patch(Polygon([[ r, ear_y0 - ear_h], [ r + ear_w, ear_y0], [ r, ear_y0 + ear_h]],
                             closed=False, edgecolor="k", linewidth=1.2, zorder=6))

    # ---------- tidy axes
    ax.set_xlim(-1.1 * r, 1.1 * r)
    ax.set_ylim(-1.1 * r, 1.1 * r)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_frame_on(False)

    # ---------- colorbar
    cbar = None
    if show_colorbar:
        mappable = cf if cf is not None else im
        cbar = plt.colorbar(mappable, ax=ax, fraction=0.046, pad=0.04, label = 'Power ($\mu^2$)')
        cbar.ax.tick_params(labelsize=9)

    return ax, im, cbar

def p_value_text_gen(p = 0.5, max_dig = 3):

    if p > 0.1:

        return 'n.s.'
    
    elif p > 0.1 ** max_dig:

        return f'p = {np.round(p, max_dig)}'
    
    else:

        return f'p < {np.round(0.1 ** max_dig, max_dig)}'
    
def significance_label_generator(pV):

    print(pV)

    if pV > 0.1:

        return 'n.s.'
    
    elif pV > 0.05:

        return '$\dag$'
    
    elif pV > 0.01:

        return '*'
    
    else:

        return '*' * np.min([int(-1 * np.log(pV) / np.log(10)), 3])