export function worldModelPosterior(prior:number,likelihoodRatio:number):number{
 if(!Number.isFinite(prior)||prior<0||prior>1)throw new Error('prior must be within [0,1]');
 if(!Number.isFinite(likelihoodRatio)||likelihoodRatio<=0)throw new Error('likelihood ratio must be positive');
 if(prior===0||prior===1)return prior;
 return (prior*likelihoodRatio)/(prior*likelihoodRatio+(1-prior));
}

export function binaryEntropy(probability:number):number{
 if(!Number.isFinite(probability)||probability<0||probability>1)throw new Error('probability must be within [0,1]');
 if(probability===0||probability===1)return 0;
 return -(probability*Math.log2(probability)+(1-probability)*Math.log2(1-probability));
}
