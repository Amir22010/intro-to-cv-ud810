import numpy as np
import cv2

def disparity_ncorr(L, R, template_size=3):
    """Compute disparity map D(y, x) such that: L(y, x) = R(y, x + D(y, x))

    Params:
    L: Grayscale left image
    R: Grayscale right image, same size as L

    Returns: Disparity map, same size as L, R
    """

    im_rows = L.shape[0]; im_cols = L.shape[1]
    tpl_rows = tpl_cols = template_size
    D_L = np.ndarray((im_rows - tpl_rows + 1, im_cols - tpl_cols + 1),
                     dtype=np.float32)
    for r in range(D_L.shape[0]):
        for c in range(D_L.shape[1]):
            tpl = L[r:r+tpl_rows, c:c+tpl_cols].astype(np.float32)
            R_strip = R[r:r+tpl_rows, :].astype(np.float32)
            res = cv2.matchTemplate(R_strip, tpl,
                                    method=cv2.TM_CCOEFF_NORMED)
            _,_,_,max_loc = cv2.minMaxLoc(res)
            D_L[r, c] = max_loc[0] - c
    return D_L
