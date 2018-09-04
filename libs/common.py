'''
Common names and conventions to reference. Mostly constant variables.
'''


#side constants
LEFT   = 'l'
RIGHT  = 'r'
CENTER = 'c'

SIDES   = {"left" : LEFT, "right" : RIGHT,
            "center" : CENTER}

#location constants
FRONT   = 'fr'
BACK    = 'bk'
MIDDLE  = 'md'
TOP     = 'tp'
BOTTOM  = 'bt'

LOCATIONS = {'front' : FRONT, 'back' : BACK, 'middle' : MIDDLE,
         'top': TOP, 'bottom' : BOTTOM}

#Class constants
IK                = "ik"
FK                = "fk"
SKELETON          = "sk"
SKINCLUSTER       = "sc"
SIMULATION        = "sim"
SKINMUSCLE        = "sam"
DRIVER            = "drv"
PSD               = "psd"
SURFACE           = "srf"
CLUSTER           = "cluster"
WIRE              = "wire"
BLEND             = "blend"
LATTICE           = "lattice"
BEND              = "bend"
CURVE             = "crv"
GUIDES            = 'guide'
POLYGON           = "mesh"
NURBS             = "nurbs"
ANCHOR            = "anchor"
ROOT              = "root"
PARENTCONSTRAINT  = "parentConstraint"
POINTCONSTRAINT   = "pointConstraint"
POINTONCURVEINFO  = "pointOnCurveInfo"
ORIENTCONSTRAINT  = "orientConstraint"
AIMCONSTRAINT     = "aimConstraint"
PAIRBLEND         = "pairBlend"
FOLLICLE          = "follicle"
MULTIPLYDIVIDE    = "multiplyDivide"
MULTDOUBLELINEAR  = "multDoubleLinear"
PLUSMINUSAVERAGE  = "plusMinusAverage"
CURVEINFO         = "curveInfo"
DISTANCEBETWEEN   = "distanceBetween"
VECTORPRODUCT     = "vpn"
DECOMPOSEROTATION = "dcr"
DECOMPOSEMATRIX   = 'dcm'
SPREAD            = "spread"
SCALE             = "scale"
ROTATE            = "rotate"
TRANSLATE         = "translate"
REMAP             = "remap"
PIVOT             = "pivot"
PIN               = "pin"
REVERSE           = "reverse"
TWEAK             = "twk"
SETRANGE          = "setRange"
UPOBJECT          = "upObject"
TARGET            = "tgt"
TWIST             = "twst"
POLEVECTOR        = "pv"
GIMBAL            = "gimbal"
CONDITION         = "condition"
SET               = "set"
AIM               = 'aim'
UP                = 'up'


#Type constants
ZERO         = "zero"
GEOMETRY     = "geo"
JOINT        = "jnt"
GROUP        = "grp"
LOCATOR      = "loc"
IKHANDLE     = "ikHandle"
EFFECTOR     = "effector"
LOCALCONTROL = "ltrl"
CONTROL      = "ctrl"
DEFORMER     = "def"
HANDLE       = "hdl"
UTILITY      = "util"
MASTER       = "master"
SHAPE        = "shape"
DISPLAYLINE  = "displayLine"



# LOD constants
HI      = "hi"
MEDIUM  = "md"
LOW     = "lo"

LODS = {"hi" : HI, "medium" : MEDIUM, "low" : LOW}


#Naming template variables
DELIMITER = "_"
NAMETEMPLATE  = "SIDE.LOCATION.DESCRIPTION.NUMBER.CLASS.TYPE"
PADDING = 3
REQUIRED = ["SIDE", "DESCRIPTION", "TYPE"]


# Color constants
NONE        = 0;    NONE_RGB        = [0, 0.015, 0.375]
BLACK       = 1;    BLACK_RGB       = [0, 0, 0]
DARKGREY    = 2;    DARKGREY_RGB    = [0.25, 0.25, 0.25] 
GREY        = 3;    GREY_RGB        = [0.5, 0.5, 0.5] 
CERISE      = 4;    CERISE_RGB      = [0.6, 0, 0.157]
DARKBLUE    = 5;    DARKBLUE_RGB    = [0, 0.016, 0.376]
BLUE        = 6;    BLUE_RGB        = [0, 0, 1]
FORESTGREEN = 7;    FORESTGREEN_RGB = [0, 0.275, 0.098]
DARKVIOLET  = 8;    DARKVIOLET_RGB  = [0.149, 0, 0.263]
MAGENTA     = 9;    MAGENTA_RGB     = [0.784, 0, 0.784]
SIENNA      = 10;   SIENNA_RGB      = [0.541, 0.282, 0.2]
BROWN       = 11;   BROWN_RGB       = [0.247, 0.137, 0.122]
DARKRED     = 12;   DARKRED_RGB     = [0.6, 0.149, 0]
RED         = 13;   RED_RGB         = [1, 0, 0]
GREEN       = 14;   GREEN_RGB       = [0, 1, 0]
MIDBLUE     = 15;   MIDBLUE_RGB     = [0, 0.255, 0.6]
WHITE       = 16;   WHITE_RGB       = [1, 1, 1] 
YELLOW      = 17;   YELLOW_RGB      = [1, 1, 0]
CYAN        = 18;   CYAN_RGB        = [0.392, 0.863, 1]
PALEGREEN   = 19;   PALEGREEN_RGB   = [0.263, 1, 0.639]
SALMON      = 20;   SALMON_RGB      = [1, 0.69, 0.69]
MOCCA       = 21;   MOCCA_RGB       = [0.894, 0.675, 0.475]
PALEYELLOW  = 22;   PALEYELLOW_RGB  = [1, 1, 0.388]
SEAGREEN    = 23;   SEAGREEN_RGB    = [0, 0.6, 0.329]
DARKGOLD    = 24;   DARKGOLD_RGB    = [0.631, 0.412, 0.188]
OLIVE       = 25;   OLIVE_RGB       = [0.624, 0.631, 0.188]
LAWNGREEN   = 26;   LAWNGREEN_RGB   = [0.408, 0.631, 0.188]
DARKGREEN   = 27;   DARKGREEN_RGB   = [0.188, 0.631, 0.365]
TURQUOISE   = 28;   TURQUOISE_RGB   = [0.188, 0.631, 0.631]
DODGERBLUE  = 29;   DODGERBLUE_RGB  = [0.188, 0.404, 0.631]
VIOLET      = 30;   VIOLET_RGB      = [0.435, 0.188, 0.631]
DARKPINK    = 31;   DARKPINK_RGB    = [0.631, 0.188, 0.412]

COLORSSTR   = ['none', 'black', 'darkgrey', 'grey', 'cerise', 'darkblue', 'blue',
               'forestgreen', 'darkviolet', 'magenta', 'sienna', 'brown', 'darkred',
               'red', 'green', 'midblue', 'white', 'yellow', 'cyan', 'palegreen',
               'salmon', 'mocca', 'paleyellow', 'seagreen', 'darkgold', 'olive',
               'lawngreen', 'darkgreen', 'turquoise', 'dodgerblue', 'violet', 'darkpink']

COLORSDICTINDEX = dict( (c, eval(c.upper())) for c in COLORSSTR) # dictionary {'colorstring': int}
COLORSDICTRGB   = dict( (c, eval('%s_RGB' % c.upper())) for c in COLORSSTR)

SIDE_COLOR  = {None: NONE, RIGHT: RED, LEFT: BLUE, CENTER: YELLOW}
SIDE_COLOR_SECONDARY  = {None: NONE, RIGHT: SALMON, LEFT: CYAN, CENTER: OLIVE}


# Component constants
VERTEX      = ".vtx"
CV          = ".cv"
EDGE        = ".e"
FACE        = ".f"
COMPONENTS  = {"vertex" : VERTEX, "cv" : CV, "edge" : EDGE, "face" : POLYGON}

# File constants
MB      = ".mb"
MA      = ".ma"
FBX     = ".fbx"
XML     = ".xml"
CLIP    = ".clip"


def toList(values):
    '''
    '''
    if not isinstance(values, (list,tuple)):
        values = [values]

    return values

def getMirrorName(name):
    mirror = name
    
    if '_l_' in name:
        mirror = name.replace('_l_', '_r_')
    elif '_r_' in name:
        mirror = name.replace('_r_', '_l_')
    elif name.endswith('_l'):
        mirror = name[:-2]+'_r'
    elif name.endswith('_r'):
        mirror = name[:-2]+'_l'
        
    return mirror

def getSideToken(name):
    token = None
    if '_l_' in name:
        token = 'l'
    elif '_r_' in name:
        token = 'r'
    elif name.endswith('_l'):
        token = 'l'
    elif name.endswith('_r'):
        token = 'r'
        
    return token
