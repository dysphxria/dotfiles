static const char norm_fg[] = "#c3c2c6";
static const char norm_bg[] = "#0F120D";
static const char norm_border[] = "#88878a";

static const char sel_fg[] = "#c3c2c6";
static const char sel_bg[] = "#504E4E";
static const char sel_border[] = "#c3c2c6";

static const char urg_fg[] = "#c3c2c6";
static const char urg_bg[] = "#4A5333";
static const char urg_border[] = "#4A5333";

static const char *colors[][3]      = {
    /*               fg           bg         border                         */
    [SchemeNorm] = { norm_fg,     norm_bg,   norm_border }, // unfocused wins
    [SchemeSel]  = { sel_fg,      sel_bg,    sel_border },  // the focused win
    [SchemeUrg] =  { urg_fg,      urg_bg,    urg_border },
};
