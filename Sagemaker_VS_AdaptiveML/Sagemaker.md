import React from 'react';
import { Database, Settings, Target, Brain, CheckCircle, Users, Server, Activity, RefreshCw, AlertTriangle, Sparkles, ArrowRight, ArrowDown, ArrowLeft } from 'lucide-react';

const RLPipelineDiagram = () => {
  const Block = ({ icon: Icon, title, color, stage }) => (
    <div className="flex flex-col items-center w-[180px]">
      <div className={`${color} p-4 rounded-xl shadow-lg w-full transform transition-all duration-300 hover:scale-105 hover:shadow-xl`}>
        <div className="flex flex-col items-center gap-2 text-center">
          <div className="bg-white/20 p-2.5 rounded-lg backdrop-blur-sm">
            <Icon className="w-6 h-6 text-white" strokeWidth={2.5} />
          </div>
          <h3 className="text-white font-semibold text-xs leading-tight px-1">{title}</h3>
        </div>
      </div>
      {stage && (
        <div className="mt-1.5 text-[10px] font-bold text-indigo-400 uppercase tracking-wider">{stage}</div>
      )}
    </div>
  );

  const HArrow = ({ direction = 'right' }) => (
    <div className="flex items-center justify-center mx-2">
      {direction === 'right' ? (
        <ArrowRight className="w-5 h-5 text-indigo-400" strokeWidth={3} />
      ) : (
        <ArrowLeft className="w-5 h-5 text-indigo-400" strokeWidth={3} />
      )}
    </div>
  );

  const VArrow = () => (
    <div className="flex flex-col items-center justify-center my-2">
      <ArrowDown className="w-5 h-5 text-indigo-400" strokeWidth={3} />
    </div>
  );

  const CornerArrow = ({ direction = 'down-left' }) => (
    <div className="flex items-center justify-center mx-2">
      <svg width="40" height="60" viewBox="0 0 40 60">
        {direction === 'down-left' ? (
          <>
            <path d="M 35 0 L 35 30 L 5 30 L 5 55" stroke="#818cf8" strokeWidth="3" fill="none" />
            <polygon points="5,60 0,50 10,50" fill="#818cf8" />
          </>
        ) : (
          <>
            <path d="M 5 0 L 5 30 L 35 30 L 35 55" stroke="#818cf8" strokeWidth="3" fill="none" />
            <polygon points="35,60 30,50 40,50" fill="#818cf8" />
          </>
        )}
      </svg>
    </div>
  );

  const SplitArrow = () => (
    <div className="flex flex-col items-center my-2">
      <svg width="60" height="50" viewBox="0 0 60 50">
        <path d="M 30 0 L 30 15 M 30 15 L 15 30 M 30 15 L 45 30" stroke="#818cf8" strokeWidth="3" fill="none" />
        <polygon points="15,35 10,25 20,25" fill="#818cf8" />
        <polygon points="45,35 40,25 50,25" fill="#818cf8" />
      </svg>
    </div>
  );

  const MergeArrow = () => (
    <div className="flex flex-col items-center my-2">
      <svg width="60" height="50" viewBox="0 0 60 50">
        <path d="M 15 0 L 30 15 M 45 0 L 30 15 M 30 15 L 30 45" stroke="#818cf8" strokeWidth="3" fill="none" />
        <polygon points="30,50 25,40 35,40" fill="#818cf8" />
      </svg>
    </div>
  );

  return (
    <div className="w-full min-h-screen bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 p-8 flex items-center justify-center">
      <div className="w-full max-w-7xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20 mb-3">
            <Sparkles className="w-4 h-4 text-indigo-400" />
            <span className="text-sm font-medium text-white/90">Enterprise ML Pipeline</span>
          </div>
          <h1 className="text-3xl font-bold text-white mb-1">
            RL Training Pipeline
          </h1>
          <p className="text-indigo-300 text-sm">Continuous Learning & Deployment Workflow</p>
        </div>

        {/* Main Pipeline - S-Flow */}
        <div className="bg-white/5 backdrop-blur-sm rounded-3xl border border-white/10 p-8">
          {/* Row 1 - Left to Right */}
          <div className="flex items-start justify-start mb-4">
            <Block 
              icon={Settings} 
              title="Policies & Regulations" 
              color="bg-gradient-to-br from-purple-500 to-purple-700"
              stage="Input"
            />
            <HArrow />
            <Block 
              icon={Database} 
              title="Datasets" 
              color="bg-gradient-to-br from-blue-500 to-blue-700"
              stage="Data"
            />
            <HArrow />
            <Block 
              icon={Target} 
              title="Golden Dataset" 
              color="bg-gradient-to-br from-amber-500 to-amber-700"
              stage=""
            />
            <HArrow />
            <Block 
              icon={Brain} 
              title="Custom RL Environment" 
              color="bg-gradient-to-br from-cyan-500 to-cyan-700"
              stage="Setup"
            />
            <HArrow />
            <Block 
              icon={Settings} 
              title="State + Action Space" 
              color="bg-gradient-to-br from-teal-500 to-teal-700"
              stage=""
            />
            <div className="w-[180px]"></div>
          </div>

          {/* Corner transition */}
          <div className="flex justify-end mr-[100px]">
            <CornerArrow direction="down-left" />
          </div>

          {/* Row 2 - Right to Left */}
          <div className="flex items-start justify-end mb-4">
            <div className="w-[180px]"></div>
            <Block 
              icon={CheckCircle} 
              title="Approval Gate" 
              color="bg-gradient-to-br from-emerald-500 to-emerald-700"
              stage=""
            />
            <HArrow direction="left" />
            <div className="flex flex-col items-center gap-2">
              <Block 
                icon={Brain} 
                title="AI / Rule Judges" 
                color="bg-gradient-to-br from-pink-500 to-pink-700"
                stage="Evaluate"
              />
              <Block 
                icon={Users} 
                title="Human Review" 
                color="bg-gradient-to-br from-rose-500 to-rose-700"
                stage=""
              />
            </div>
            <HArrow direction="left" />
            <Block 
              icon={CheckCircle} 
              title="Evaluation vs Golden" 
              color="bg-gradient-to-br from-violet-500 to-violet-700"
              stage=""
            />
            <HArrow direction="left" />
            <Block 
              icon={Brain} 
              title="RL Training (PPO)" 
              color="bg-gradient-to-br from-indigo-500 to-indigo-700"
              stage="Training"
            />
            <HArrow direction="left" />
            <Block 
              icon={Target} 
              title="Reward Function" 
              color="bg-gradient-to-br from-green-500 to-green-700"
              stage=""
            />
          </div>

          {/* Corner transition */}
          <div className="flex justify-start ml-[100px]">
            <CornerArrow direction="down-right" />
          </div>

          {/* Row 3 - Left to Right */}
          <div className="flex items-start justify-start">
            <div className="w-[180px]"></div>
            <Block 
              icon={Server} 
              title="SageMaker Endpoint" 
              color="bg-gradient-to-br from-blue-500 to-blue-700"
              stage="Deploy"
            />
            <HArrow />
            <Block 
              icon={Activity} 
              title="Monitoring + Drift" 
              color="bg-gradient-to-br from-orange-500 to-orange-700"
              stage="Monitor"
            />
            <HArrow />
            <Block 
              icon={AlertTriangle} 
              title="Retraining Trigger" 
              color="bg-gradient-to-br from-red-500 to-red-700"
              stage=""
            />
            <div className="flex items-center mx-4">
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-5 py-3 rounded-xl shadow-xl flex items-center gap-2 border-2 border-indigo-400/50">
                <RefreshCw className="w-5 h-5 text-white animate-spin" style={{animationDuration: '4s'}} />
                <span className="font-semibold text-white text-sm whitespace-nowrap">Loop Back</span>
              </div>
            </div>
          </div>
        </div>

        {/* Footer Stats */}
        <div className="mt-6 flex justify-center gap-6">
          <div className="bg-white/10 backdrop-blur-sm rounded-xl px-6 py-3 border border-white/20">
            <div className="text-indigo-400 font-bold text-xl">7</div>
            <div className="text-white/70 text-xs">Stages</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-xl px-6 py-3 border border-white/20">
            <div className="text-indigo-400 font-bold text-xl">14</div>
            <div className="text-white/70 text-xs">Steps</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-xl px-6 py-3 border border-white/20">
            <div className="text-indigo-400 font-bold text-xl">∞</div>
            <div className="text-white/70 text-xs">Loop</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RLPipelineDiagram;