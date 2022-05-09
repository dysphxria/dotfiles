const char *colorname[] = {

  /* 8 normal colors */
  [0] = "#0F120D", /* black   */
  [1] = "#4A5333", /* red     */
  [2] = "#504E4E", /* green   */
  [3] = "#696669", /* yellow  */
  [4] = "#82816D", /* blue    */
  [5] = "#797585", /* magenta */
  [6] = "#837C8A", /* cyan    */
  [7] = "#c3c2c6", /* white   */

  /* 8 bright colors */
  [8]  = "#88878a",  /* black   */
  [9]  = "#4A5333",  /* red     */
  [10] = "#504E4E", /* green   */
  [11] = "#696669", /* yellow  */
  [12] = "#82816D", /* blue    */
  [13] = "#797585", /* magenta */
  [14] = "#837C8A", /* cyan    */
  [15] = "#c3c2c6", /* white   */

  /* special colors */
  [256] = "#0F120D", /* background */
  [257] = "#c3c2c6", /* foreground */
  [258] = "#c3c2c6",     /* cursor */
};

/* Default colors (colorname index)
 * foreground, background, cursor */
 unsigned int defaultbg = 0;
 unsigned int defaultfg = 257;
 unsigned int defaultcs = 258;
 unsigned int defaultrcs= 258;
