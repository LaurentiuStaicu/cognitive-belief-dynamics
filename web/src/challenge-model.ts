import type {M1AccessData} from './access-stage';

export type AccessChallengeProjection={
 experimentId:string;
 purpose:string;
 storyId:string;
 sourceId:string;
 imageId:string|null;
 previewImpression:boolean;
 controlCue:number;
 treatmentCue:number;
 betaHneg:number;
 calibrated:boolean;
 nullModel:{lower:number;higher:number;delta:number};
 alternativeModel:{lower:number;higher:number;delta:number};
 empiricalTargetId:string;
 validationPatternIds:string[];
 interpretationBoundary:string;
};

export function projectAccessChallenge(data:M1AccessData):AccessChallengeProjection{
 const experiment=data.experiment;
 const lower=experiment.conditions.lower_negativity;
 const higher=experiment.conditions.higher_negativity;
 const invariant=(field:'story_id'|'source_id'|'image_id'|'preview_impression')=>{
  if(lower[field]!==higher[field])throw new Error(`M1.E3 Challenge Model invariant failed: ${field}`);
 };
 invariant('story_id');
 invariant('source_id');
 invariant('image_id');
 invariant('preview_impression');
 if(lower.hneg!==experiment.cue_encoding.control||higher.hneg!==experiment.cue_encoding.treatment){
  throw new Error('M1.E3 Challenge Model cue encoding mismatch');
 }
 const nullDelta=higher.models.null.p_access-lower.models.null.p_access;
 if(Math.abs(nullDelta)>1e-12)throw new Error('M1.E3 NULL comparator no longer preserves the registered access-gate null');
 return {
  experimentId:experiment.id,
  purpose:experiment.purpose,
  storyId:lower.story_id,
  sourceId:lower.source_id,
  imageId:lower.image_id,
  previewImpression:lower.preview_impression,
  controlCue:experiment.cue_encoding.control,
  treatmentCue:experiment.cue_encoding.treatment,
  betaHneg:experiment.parameters.beta_hneg,
  calibrated:experiment.parameters.calibrated,
  nullModel:{lower:lower.models.null.p_access,higher:higher.models.null.p_access,delta:nullDelta},
  alternativeModel:{
   lower:lower.models.headline_negativity.p_access,
   higher:higher.models.headline_negativity.p_access,
   delta:higher.models.headline_negativity.p_access-lower.models.headline_negativity.p_access
  },
  empiricalTargetId:experiment.empirical_target_id,
  validationPatternIds:[...experiment.validation_pattern_ids],
  interpretationBoundary:experiment.interpretation_boundary
 };
}
