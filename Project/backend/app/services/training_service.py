"""Training service for simulating training jobs."""

import asyncio
import random
import uuid
from datetime import datetime

from app.models.experiment import Experiment, ExperimentStatus
from app.models.evaluation import Evaluation
from app.models.model import Model, ModelType
from app.config import settings
from app.database import SessionLocal


async def simulate_training(experiment_id: str):
    """
    Simulate a training job.
    
    Args:
        experiment_id: ID of the experiment
    """
    db = SessionLocal()
    try:
        # Wait before changing to "running"
        await asyncio.sleep(settings.training_simulation_delay)
        
        # Update status to running
        experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
        if not experiment:
            return
        
        experiment.status = ExperimentStatus.RUNNING
        db.commit()
        
        # Simulate training duration
        await asyncio.sleep(settings.training_simulation_duration)
        
        # Refresh experiment
        db.refresh(experiment)
        
        # Randomly succeed or fail (90% success rate)
        if random.random() < 0.9:
            experiment.status = ExperimentStatus.COMPLETED
            
            # Create resulting model
            resulting_model = Model(
                name=f"{experiment.name}_trained",
                model_type=ModelType.FINE_TUNED,
                base_model_id=experiment.base_model_id,
                version="1.0.0",
                architecture="transformer",
                parameters_count=random.randint(1000000, 100000000),
                description=f"Fine-tuned model from experiment {experiment.name}",
                is_latest_version=True
            )
            db.add(resulting_model)
            db.flush()
            
            experiment.resulting_model_id = resulting_model.id
            
            # Create evaluation
            metrics = {
                "accuracy": round(random.uniform(0.75, 0.95), 4),
                "f1": round(random.uniform(0.70, 0.90), 4),
                "perplexity": round(random.uniform(10.0, 50.0), 4)
            }
            
            # Generate loss curve data
            epochs = experiment.training_config.get("epochs", 10)
            train_loss = [random.uniform(2.0, 0.1) * (1 - i/epochs) for i in range(epochs)]
            val_loss = [l + random.uniform(0, 0.2) for l in train_loss]
            
            loss_curve = {
                "epochs": list(range(1, epochs + 1)),
                "train_loss": train_loss,
                "val_loss": val_loss
            }
            
            training_statistics = {
                "total_epochs": epochs,
                "final_train_loss": train_loss[-1],
                "final_val_loss": val_loss[-1],
                "training_time_seconds": settings.training_simulation_duration
            }
            
            evaluation = Evaluation(
                experiment_id=experiment_id,
                metrics=metrics,
                loss_curve=loss_curve,
                training_statistics=training_statistics
            )
            db.add(evaluation)
            
        else:
            experiment.status = ExperimentStatus.FAILED
        
        db.commit()
        
    except Exception as e:
        # Mark as failed on error
        try:
            experiment = db.query(Experiment).filter(Experiment.id == experiment_id).first()
            if experiment:
                experiment.status = ExperimentStatus.FAILED
                db.commit()
        except:
            pass
        print(f"Training simulation error: {e}")
    finally:
        db.close()
