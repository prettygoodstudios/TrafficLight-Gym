from environment import  Environment
from agents.agent import Agent
from loggers.logger import Logger

def runner(environment: Environment, agent: Agent, logger: Logger, maxEpisodeLength: int = 500) -> None:
    for _ in range(maxEpisodeLength):
        action = agent.act(environment.state)
        state, reward, done = environment.step(action)
        agent.update(action, state, reward)
        logger.logStep(action, state, reward)
        environment.render()
        if done:
            break
    logger.logEpisode(agent)
