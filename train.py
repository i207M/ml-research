from trainers.trainer_cifar import CifarTrainer
from utils.yaml import add_arguments

if __name__ == "__main__":
    args = add_arguments()

    trainer = CifarTrainer(args)
    trainer.train()
