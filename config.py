import logging
from redis import StrictRedis


class Config(object):  # object配置信息的基类
    """项目配置参数"""

    SECRET_KEY = "nn2zJQYyJWCOITgKDf5CsAFBsPixuOpWzJ0Haii5F61H5fais9G1cijn5an3WRzu"

    # 为数据库添加配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/information"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 是否开启sql语句追踪
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # redis的配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # Session保存配置
    SESSION_TYPE = "redis"
    # 开启session签名(保护)
    SESSION_USE_SIGNER = True
    # 指定session保存的redis
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    # 设置需要过期
    SESSION_PERMANENT = False
    # 设置过期时间
    PERMANENT_SESSION_LIFETIME = 86400 * 2

    # 设置日志等级
    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(Config):
    """开发环境下的配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境下的配置"""
    DEBUG = False
    # 生产环境下的数据库配置
    LOG_LEVEL = logging.WARNING


class TestingConfig(Config):
    """单元测试下的环境配置"""
    DEBUG = True
    TESTING = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
