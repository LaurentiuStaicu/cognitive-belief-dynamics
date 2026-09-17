export const calibrationExtension={
 status:'PLANNED_POST_V1',
 mounted:false,
 route:null,
 uploadControlAvailable:false,
 acceptedExtensions:['.txt','.md','.csv','.tsv','.json','.xlsx','.ods'] as const,
 principle:'Calibration remains outside the pre-v1 runtime while a typed extension seam is retained.'
} as const;

export type CalibrationAcceptedExtension=typeof calibrationExtension.acceptedExtensions[number];

export type CalibrationSourceFile={
 name:string;
 extension:CalibrationAcceptedExtension;
 mimeType:string;
 sizeBytes:number;
};

export type CalibrationInputBundle={
 files:CalibrationSourceFile[];
 modelSpecification:string;
 evidenceSnapshot:string;
 importedAt:string;
};

export type CalibrationValidationResult={
 valid:boolean;
 errors:string[];
 warnings:string[];
 detectedFields:string[];
};

export type CalibrationResultManifest={
 calibrationId:string;
 modelSpecification:string;
 evidenceSnapshot:string;
 sourceFiles:CalibrationSourceFile[];
 parameterIds:string[];
 diagnostics:string[];
 createdAt:string;
};

export interface CalibrationModulePort{
 validate(bundle:CalibrationInputBundle):Promise<CalibrationValidationResult>;
 calibrate(bundle:CalibrationInputBundle):Promise<CalibrationResultManifest>;
}
