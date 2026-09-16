export const visualLanguage={
 spacing:{
  unitPx:6,
  contentMarginMinPx:12,
  scalePx:[6,12,18,24,36,48] as const
 },
 typography:{
  fontStack:'system-ui, Inter, sans-serif',
  readerMaxCh:72,
  bodyLineHeight:1.6
 },
 interaction:{
  targetMinPx:44,
  focusRingPx:3,
  focusOffsetPx:3
 },
 breakpointsPx:{
  compact:760,
  medium:1050
 },
 chartSeries:{
  belief:{cssVar:'--series-belief',dash:'none',label:'belief'},
  sharing:{cssVar:'--series-sharing',dash:'8 4',label:'sharing'},
  correction:{cssVar:'--series-correction',dash:'2 4',label:'correction'}
 },
 epistemicMarkers:{
  EMPIRICAL:'E',
  EXECUTABLE:'X',
  CONCEPTUAL:'C',
  INTERPRETIVE:'I',
  EXPERIMENTAL:'EX',
  META_ANALYTIC:'MA',
  CANDIDATE:'?',
  REFERENCE_CANDIDATE:'R'
 }
} as const;

export const chartSeries=visualLanguage.chartSeries;
export type EpistemicStatus=keyof typeof visualLanguage.epistemicMarkers;
