
import numpy as np
from scipy.interpolate import griddata
import math

class extra__surf():
    """extra__surf.
    """


    def __init__(self, C):
        """__init__.

        Parameters
        ----------
        C :
            C
        """
        self.COEF = C[1]
        self.user_surface = C[0]
        self.user_derivative = None
        if len(C) > 2:
            self.user_derivative = C[2]

    def calculate(self, x, y):
        """calculate.

        Parameters
        ----------
        x :
            x
        y :
            y
        """
        Z = self.user_surface(x, y, self.COEF)
        return Z

    def derivative(self, x, y):
        """Return an optional user-provided sag derivative.

        Existing ExtraData surfaces only provide ``calculate`` and therefore
        keep using the numerical derivative fallback. Users who need analytic
        performance can pass ``ExtraData = [surface, coef, derivative]`` where
        derivative returns ``(dzdx, dzdy)``.
        """
        if self.user_derivative is None:
            return None
        return self.user_derivative(x, y, self.COEF)


class aspheric__surf():
    """aspheric__surf.
    """
    def __init__(self, E):
        """__init__.

        Parameters
        ----------
        E :
            E
        """
        self.E = E

    def calculate(self, x, y):
        """calculate.

        Parameters
        ----------
        x :
            x
        y :
            y
        """

        r = np.sqrt(((x * x) + (y * y)))
        Z = 0.0 * np.zeros_like(x)
        for i in range(1, 9):
            if (self.E[(i - 1)] != 0):
                Z = (Z + (self.E[(i - 1)] * np.power(r, ((2.0 * i*1.0) * 1.0))))

        return Z

    def derivative(self, x, y):
        """Return the analytical derivative of the polynomial asphere sag."""
        scalar_input = np.isscalar(x) and np.isscalar(y)
        dzdx = 0.0 if scalar_input else 0.0 * np.zeros_like(x)
        dzdy = 0.0 if scalar_input else 0.0 * np.zeros_like(y)
        r2 = ((x * x) + (y * y))
        for i in range(1, 9):
            coef = self.E[(i - 1)]
            if (coef != 0):
                power = 2.0 * i
                radial = np.power(r2, ((power - 2.0) / 2.0))
                dzdx = dzdx + (coef * power * x * radial)
                dzdy = dzdy + (coef * power * y * radial)
        return dzdx, dzdy

class conic__surf(object):
    """conic__surf.
    """
    def __init__(self, R_C, KON, C_RXY_RATIO):
        """__init__.

        Parameters
        ----------
        R_C :
            R_C
        KON :
            KON
        C_RXY_RATIO :
            C_RXY_RATIO
        """
        self.R_C = R_C
        self.KON = KON
        self.C_RXY_RATIO = C_RXY_RATIO

    def calculate(self, x, y):
        """calculate.

        Parameters
        ----------
        x :
            x
        y :
            y
        """

        if (self.R_C != 0.0):

            s = np.sqrt(((x * x) + ((y * self.C_RXY_RATIO) * (y * self.C_RXY_RATIO))))

            c = (1.0 / self.R_C)
            InRoot = (1 - (((((self.KON + 1.0) * c) * c) * s) * s))

            InRoot = np.abs(InRoot)
            z = (((c * s) * s) / (1.0 + np.sqrt(InRoot)))
        else:
            z = 0.0 * np.zeros_like(x)

        return z

    def derivative(self, x, y):
        """Return the analytical derivative of the conic sag.

        The formula follows ``calculate`` exactly, including the historical
        ``abs`` inside the square root. If the derivative is singular at the
        conic limit, ``None`` is returned so the caller can use the established
        finite-difference path.
        """
        if (self.R_C == 0.0):
            return 0.0 * np.zeros_like(x), 0.0 * np.zeros_like(y)

        c = (1.0 / self.R_C)
        q = self.C_RXY_RATIO
        s2 = ((x * x) + ((y * q) * (y * q)))
        root_arg = (1.0 - (((self.KON + 1.0) * c * c) * s2))

        if np.isscalar(root_arg):
            root = math.sqrt(abs(root_arg))
            if root == 0:
                return None
            root_sign = 1.0 if root_arg > 0 else -1.0
            droot_ds2 = ((- (self.KON + 1.0) * c * c * root_sign) / (2.0 * root))
            dz_ds2 = (c / (1.0 + root)) - ((c * s2 * droot_ds2) / ((1.0 + root) ** 2.0))
            dzdx = dz_ds2 * 2.0 * x
            dzdy = dz_ds2 * 2.0 * y * (q * q)
            return dzdx, dzdy

        x = np.asarray(x)
        y = np.asarray(y)
        root_abs = np.abs(root_arg)
        root = np.sqrt(root_abs)

        if np.any(root == 0):
            return None

        root_sign = np.sign(root_arg)
        droot_ds2 = ((- (self.KON + 1.0) * c * c * root_sign) / (2.0 * root))
        dz_ds2 = (c / (1.0 + root)) - ((c * s2 * droot_ds2) / ((1.0 + root) ** 2.0))

        dzdx = dz_ds2 * 2.0 * x
        dzdy = dz_ds2 * 2.0 * y * (q * q)
        return dzdx, dzdy



class axicon__surf():
    """axicon__surf.
    """

    def __init__(self, C_RXY_RATIO, AXC):
        """__init__.

        Parameters
        ----------
        C_RXY_RATIO :
            C_RXY_RATIO
        AXC :
            AXC
        """
        self.C_RXY_RATIO = C_RXY_RATIO
        self.AXC = AXC

    def calculate(self, x, y):
        """calculate.

        Parameters
        ----------
        x :
            x
        y :
            y
        """

        if (self.AXC != 0.0):
            s = np.sqrt(((x * x) + ((y * self.C_RXY_RATIO) * (y * self.C_RXY_RATIO))))
            z_axicon = (s * np.tan(np.deg2rad(self.AXC)))
        else:
            z_axicon = 0.0 * np.zeros_like(x)

        return z_axicon

    def derivative(self, x, y):
        """Return the analytical derivative of the axicon sag.

        The axicon apex is singular. At exactly ``r=0`` the method returns
        ``None`` so callers preserve the previous numerical behavior.
        """
        if (self.AXC == 0.0):
            return 0.0 * np.zeros_like(x), 0.0 * np.zeros_like(y)

        q = self.C_RXY_RATIO
        s = np.sqrt(((x * x) + ((y * q) * (y * q))))
        if np.isscalar(s):
            if s == 0:
                return None
            slope = math.tan(math.radians(self.AXC))
            dzdx = slope * (x / s)
            dzdy = slope * ((y * q * q) / s)
            return dzdx, dzdy

        x = np.asarray(x)
        y = np.asarray(y)
        if np.any(s == 0):
            return None

        slope = np.tan(np.deg2rad(self.AXC))
        dzdx = slope * (x / s)
        dzdy = slope * ((y * q * q) / s)
        return dzdx, dzdy


class error_map__surf():
    """error_map__surf.
    """

    def __init__(self, xValues, yValues, zValues, SPACE):
        """__init__.

        Parameters
        ----------
        xValues :
            xValues
        yValues :
            yValues
        zValues :
            zValues
        SPACE :
            SPACE
        """
        TG = SPACE
        LGMX = np.max(yValues)
        LGMN = np.min(yValues)
        LG = (LGMX - LGMN)
        NPG = int((1 + (LG / TG)))
        s = 40
        VXX = np.arange((((- LG) / 2.0) - (s * TG)), ((LG / 2.0) + (s * TG)), TG)
        VYY = np.arange((((- LG) / 2.0) - (s * TG)), ((LG / 2.0) + (s * TG)), TG)
        NPG = VXX.shape[0]
        (grid_x, grid_y) = np.meshgrid(VXX, VYY)
        Z = np.zeros((NPG, NPG))
        err = 0.01
        cont = 1
        for h in range(0, NPG):
            for k in range(0, NPG):
                Ox = grid_x[(h, k)]
                Oy = grid_y[(h, k)]
                ARGWx = np.argwhere(((xValues < (Ox + err)) & (xValues > (Ox - err))))
                ARGWy = np.argwhere(((yValues < (Oy + err)) & (yValues > (Oy - err))))
                if ((ARGWx.shape[0] > 0) and (ARGWy.shape[0] > 0)):
                    IN = np.intersect1d(ARGWx, ARGWy)
                    if (IN.shape[0] > 0):
                        varg = IN[0]
                        Z[(h, k)] = zValues[varg]
                        cont = (cont + 1)
        pnts = np.argwhere((Z != 0.0))
        values = Z[(pnts[:, 0], pnts[:, 1])]
        Vx = VXX[pnts[:, 0]]
        Vy = VYY[pnts[:, 1]]
        points = np.vstack((Vx, Vy)).T
        aXX = np.arange((((- LG) / 2.0) - (s * TG)), ((LG / 2.0) + (s * TG)), (TG / 1.0))
        aYY = np.arange((((- LG) / 2.0) - (s * TG)), ((LG / 2.0) + (s * TG)), (TG / 1.0))
        (grid_x, grid_y) = np.meshgrid(aXX, aYY)
        grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
        Z[0, :] = grid_z0[0, :]
        Z[(NPG - 1), :] = grid_z0[(NPG - 1), :]
        Z[:, 0] = grid_z0[:, 0]
        Z[:, (NPG - 1)] = grid_z0[:, (NPG - 1)]
        pnts = np.argwhere((Z != 0.0))
        Vx = VXX[pnts[:, 0]]
        Vy = VYY[pnts[:, 1]]
        self.values = Z[(pnts[:, 0], pnts[:, 1])]
        self.points = np.vstack((Vx, Vy)).T

    def calculate(self, x, y):
        """calculate.

        Parameters
        ----------
        x :
            x
        y :
            y
        """
        z = griddata(self.points, self.values, (x, y), method='cubic')
        return z

class zernike__surf():
    """zernike__surf.
    """

    def __init__(self, COEF, Z_POL, Z_POW, DMTR):
        """__init__.

        Parameters
        ----------
        COEF :
            COEF
        Z_POL :
            Z_POL
        Z_POW :
            Z_POW
        DMTR :
            DMTR
        """
        self.COEF = COEF
        self.Z_POL = Z_POL
        self.Z_POW = Z_POW
        self.DMTR = DMTR

    def calculate(self, x, y):
        """calculate.

        Parameters
        ----------
        x :
            x
        y :
            y
        """

        ZSP = CalculateZern(x, y, self.Z_POL, self.Z_POW, self.COEF, self.DMTR)
        return ZSP

    def derivative(self, x, y):
        """Return the analytical derivative of KrakenOS Zernike sag terms.

        KrakenOS uses ``theta = arctan2(x, y)`` in ``CalculateZern``. The
        derivative intentionally follows that same convention, rather than the
        more common ``arctan2(y, x)``, so analytical and numerical slopes refer
        to the same surface definition. At the exact origin the angular
        derivative is singular, so this method returns ``None`` and lets the
        caller use finite differences.
        """
        radius = np.sqrt(((x * x) + (y * y)))
        if np.isscalar(radius):
            if radius == 0:
                return None
            return self._derivative_scalar(x, y, radius)

        x = np.asarray(x)
        y = np.asarray(y)
        if np.any(radius == 0):
            return None

        norm_radius = (self.DMTR / 2.0)
        ro = radius / norm_radius
        theta = np.arctan2(x, y)
        dro_dx = x / (norm_radius * radius)
        dro_dy = y / (norm_radius * radius)
        dtheta_dx = y / (radius * radius)
        dtheta_dy = -x / (radius * radius)

        dzdx = 0.0 * np.zeros_like(x)
        dzdy = 0.0 * np.zeros_like(y)

        for term in range(0, self.COEF.shape[0]):
            coef = self.COEF[term]
            if (coef != 0):
                (j, n, m, par, raiz) = self.Z_POL[term]
                radial, radial_der = zernike_radial_and_derivative(ro, self.Z_POW[term])

                if (par == 1):
                    dterm_dro = raiz * radial_der
                    dterm_dtheta = 0.0
                elif (par == 3):
                    trig = np.cos((m * theta))
                    dterm_dro = raiz * radial_der * trig
                    dterm_dtheta = -raiz * radial * m * np.sin((m * theta))
                elif (par == 2):
                    trig = np.sin((m * theta))
                    dterm_dro = raiz * radial_der * trig
                    dterm_dtheta = raiz * radial * m * np.cos((m * theta))
                else:
                    return None

                dzdx = dzdx + coef * ((dterm_dro * dro_dx) + (dterm_dtheta * dtheta_dx))
                dzdy = dzdy + coef * ((dterm_dro * dro_dy) + (dterm_dtheta * dtheta_dy))

        return dzdx, dzdy

    def _derivative_scalar(self, x, y, radius):
        norm_radius = (self.DMTR / 2.0)
        ro = radius / norm_radius
        theta = math.atan2(x, y)
        dro_dx = x / (norm_radius * radius)
        dro_dy = y / (norm_radius * radius)
        dtheta_dx = y / (radius * radius)
        dtheta_dy = -x / (radius * radius)

        dzdx = 0.0
        dzdy = 0.0

        for term in range(0, self.COEF.shape[0]):
            coef = self.COEF[term]
            if (coef != 0):
                (j, n, m, par, raiz) = self.Z_POL[term]
                radial, radial_der = zernike_radial_and_derivative(ro, self.Z_POW[term])

                if (par == 1):
                    dterm_dro = raiz * radial_der
                    dterm_dtheta = 0.0
                elif (par == 3):
                    trig = math.cos((m * theta))
                    dterm_dro = raiz * radial_der * trig
                    dterm_dtheta = -raiz * radial * m * math.sin((m * theta))
                elif (par == 2):
                    trig = math.sin((m * theta))
                    dterm_dro = raiz * radial_der * trig
                    dterm_dtheta = raiz * radial * m * math.cos((m * theta))
                else:
                    return None

                dzdx = dzdx + coef * ((dterm_dro * dro_dx) + (dterm_dtheta * dtheta_dx))
                dzdy = dzdy + coef * ((dterm_dro * dro_dy) + (dterm_dtheta * dtheta_dy))

        return dzdx, dzdy

def CalculateZern( x, y, Z_POL, Z_POW, COEF, DMTR):
    """calculate.

    Parameters
    ----------
    x :
        x
    y :
        y
    """
    ZSP = 0.0*np.zeros_like(x)
    for i in range(0, COEF.shape[0]):
        if (COEF[i] != 0):
            p = (np.sqrt(((x * x) + (y * y))) / (DMTR / 2.0))
            f = np.arctan2(x, y)
            ZSP = (ZSP + (COEF[i] * zernike_polynomials(i, p, f, Z_POL, Z_POW)))
    return ZSP

def zernike_polynomials(term, ro, theta, Zern_pol, z_pow):
    """zernike_polynomials.

    Parameters
    ----------
    term :
        term
    ro :
        ro
    theta :
        theta
    Zern_pol :
        Zern_pol
    z_pow :
        z_pow
    """
    (j, n, m, par, raiz) = Zern_pol[term]
    ct = z_pow[term][0]
    pot = z_pow[term][1]
    NR = 0
    L = len(ct)
    for i in range(0, L):
        NR = ((ct[i] * np.power(ro, pot[i])) + NR)

    if (par == 1):
        S = (raiz * NR)
    if (par == 3):
        S = ((raiz * NR) * np.cos((m * theta)))
    if (par == 2):
        S = ((raiz * NR) * np.sin((m * theta)))
    return S

def zernike_radial_and_derivative(ro, z_pow):
    """Return a Zernike radial polynomial and d(radial)/d(ro)."""
    ct = z_pow[0]
    pot = z_pow[1]
    radial = 0
    radial_der = 0
    for i in range(0, len(ct)):
        radial = ((ct[i] * np.power(ro, pot[i])) + radial)
        if (pot[i] != 0):
            radial_der = ((ct[i] * pot[i] * np.power(ro, (pot[i] - 1))) + radial_der)
    return radial, radial_der

def z_parity(num):
    """z_parity.

    Parameters
    ----------
    num :
        num
    """
    nv = (num / 2.0)
    n = (nv - int(nv))
    if (n == 0):
        v = 2
    else:
        v = 3
    return v

def r_zern(m, n):
    """r_zern.

    Parameters
    ----------
    m :
        m
    n :
        n
    """
    ls = int(((n - m) / 2.0))
    cont = 0
    TCV = []
    pot = []
    a = []
    for s in range(0, (int(ls) + 1)):
        # print((n - s), int(n - s),"----", ((n + m) / 2.0) - s, (int(((n + m) / 2.0) - s)),"----" ,((((n - m) / 2.0) - s)), (int(((n - m) / 2.0) - s)))
        # try:
        #     V1 = (np.power((- 1), s) * math.factorial((n - s)))
        #     V2 = ((math.factorial(s) * math.factorial((((n + m) / 2.0) - s))) * math.factorial((((n - m) / 2.0) - s)))

        # except:
        V1 = (np.power((- 1), s) * math.factorial(int(n - s)))
        V2 = ((math.factorial(s) * math.factorial(int(((n + m) / 2.0) - s))) * math.factorial(int(((n - m) / 2.0) - s)))

        TC = (V1 / V2)
        potencia = (n - (2.0 * s))
        TCV.append(TC)
        pot.append(potencia)
        cont = (cont + 1)
    a.append(TCV)
    a.append(pot)
    return a

def zernike_expand(L):
    """zernike_expand.

    Parameters
    ----------
    L :
        L
    """
    cont = 0
    Z = np.array([0, 0, 0, 0, 0])
    n = L
    m = L
    for i in range(0, n):
        if (cont >= L):
            break
        for j in range(0, m):
            v = ((j - i) / 2.0)
            if ((v - int(v)) == 0):
                if ((i > j) or (i == j)):
                    if (j != 0):
                        v = z_parity(cont)
                        Z = np.vstack((Z, [cont, i, j, v, np.sqrt((2.0 * (i + 1.0)))]))
                        if (cont >= L):
                            break
                        cont = (cont + 1)
                        v = z_parity(cont)
                        Z = np.vstack((Z, [cont, i, j, v, np.sqrt((2.0 * (i + 1.0)))]))
                        if (cont >= L):
                            break
                        cont = (cont + 1)
                    if (j == 0):
                        Z = np.vstack((Z, [cont, i, j, 1, np.sqrt((i + 1.0))]))
                        if (cont >= L):
                            break
                        cont = (cont + 1)
    Z = np.delete(Z, 0, 0)
    E = []
    for i in range(0, Z.shape[0]):
        (j, n, m, paR_c, raiz) = Z[i]
        a = r_zern(m, n)
        E.append(a)
    Z = Z[:L]
    return (Z, E)

def zernike_math_notation(term, Zern_pol, z_pow):
    """zernike_math_notation.

    Parameters
    ----------
    term :
        term
    Zern_pol :
        Zern_pol
    z_pow :
        z_pow
    """
    (j, n, m, par, raiz) = Zern_pol[term]
    ZZZ = ['Piston', 'Tilt x, (about y axis)', 'Tilt y, (about x axis)', 'Power or Focus', 'Astigmatism y, (45deg)', 'Astigmatism x, (0deg)', 'Coma y', 'Coma x', 'Trefoil y', 'Trefoil x', 'Primary Spherical', 'Secondary Astigmatism x', 'Secondary Astigmatism y', 'Tetrafoil x', 'Tetrafoil y', 'Secondary Coma x', 'Secondary Coma y', 'Secondary Trefoil x', 'Secondary Trefoil y', 'Pentafoil x', 'Pentafoil y', 'Secondary Spherical', 'Tertiary Astigmatism y', 'Tertiary Astigmatism x', 'Secondary Tetrafoil y', 'Secondary Tetrafoil x', '14^(1/2) (p^6) * SIN (6A)', '14^(1/2) (p^6) * COS (6A)', 'Tertiary Coma y', 'Tertiary Coma x', 'Tertiary Trefoil y', 'Tertiary Trefoil x']
    ct = z_pow[term][0]
    pot = z_pow[term][1]
    NR = ' '
    L = len(ct)
    for i in range(0, L):
        if (pot[i] == 0):
            NR = ((str(ct[i]) + '+') + NR)
        else:
            NR = ((((str(ct[i]) + 'r^') + str(int(pot[i]))) + '+') + NR)
    i = len(NR)
    NR = NR[:(- 2)]
    if (m == 1):
        mm = ''
    else:
        mm = str(int(m))
    if (par == 1):
        S = (((str(int((0.01 + (raiz * raiz)))) + '^(1/2)(') + NR) + ')')
    if (par == 3):
        S = ((((((str(int((0.01 + (raiz * raiz)))) + '^(1/2)(') + NR) + ')') + 'cos(') + mm) + 'T)')
    if (par == 2):
        S = ((((((str(int((0.01 + (raiz * raiz)))) + '^(1/2)(') + NR) + ')') + 'sin(') + mm) + 'T)')
    if (term < len(ZZZ)):
        x = ZZZ[[term][0]][:]
    else:
        x = ''
    return ((S + '   ') + x)

def Wavefront_Zernike_Phase(x, y, COEF):
    """Wavefront_Zernike_Phase.

    Parameters
    ----------
    x :
        x
    y :
        y
    COEF :
        COEF
    """
    NC = len(COEF)
    (Zern_pol, z_pow) = zernike_expand(NC)
    tcoef = COEF.shape[0]
    p = np.sqrt(((x * x) + (y * y)))
    f = np.arctan2(x, y)
    ZFP = 0.0
    for i in range(0, tcoef):
        if (COEF[i] != 0):
            ZFP = (ZFP + (COEF[i] * zernike_polynomials(i, p, f, Zern_pol, z_pow)))
    return ZFP
