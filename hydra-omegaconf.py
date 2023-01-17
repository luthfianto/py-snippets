from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra
from hydra.utils import to_absolute_path as abspath
from omegaconf import OmegaConf

GlobalHydra.instance().clear()
initialize(config_path="config", job_name="test_app")
config = compose(config_name="main.yaml")
