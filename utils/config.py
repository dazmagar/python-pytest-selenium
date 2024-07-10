from dataclasses import dataclass
from omegaconf import OmegaConf, DictConfig
from _pytest.config import Config as PytestConfig

import definitions


@dataclass
class Config:

    config: DictConfig = OmegaConf.load(definitions.root_path / "config.yaml")

    @classmethod
    def update_config_with_cl_args(cls, config: PytestConfig) -> None:
        cls.config = OmegaConf.merge(
            cls.config,
            {key.lstrip("-"): value for key, value in OmegaConf.from_cli(config.invocation_params.args).items()},
        )


def get_config() -> DictConfig:
    return Config.config
