from environment import  Environment
from agents.agent import Agent
from loggers.logger import Logger

def runner(environment: Environment, agent: Agent, logger: Logger, maxEpisodeLength: int = 500, stepLength: int = 1) -> None:
    steps = 0
    action = None
    reward = 0
    state = environment.state
    for _ in range(maxEpisodeLength):
        if steps % stepLength == 0:
            action = agent.act(environment.state)
        steps += 1
        nextState, newReward, done = environment.step(action)
        reward += newReward
        if steps % stepLength == 0: 
            agent.update(action, state, nextState, reward)
            logger.logStep(action, state, reward)
            state = nextState
            reward = 0
            steps = 0
        environment.render()
        if done:
            break
    agent.episodeReset()
    logger.logEpisode(agent)
