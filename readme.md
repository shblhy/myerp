# 执行方法

    pip install -r deploy/requirment.txt
    在myerp.settings.DATABASES配置下数据库，这里用的是mysql数据库
    python manage.py migrate
    python manage.py createsuperuser 创建用户 root 987654321
    python manage.py runserver 0.0.0.0:8000
    http://0.0.0.0:8000/admin   输入用户名密码登录
    http://0.0.0.0:8000/admin/meeting/meetingroom/ 会议室列表（django管理后台界面）
    http://0.0.0.0:8000/admin/meeting/meeting/ 会议列表（django管理后台界面）
    http://0.0.0.0:8000/meeting/meetingroom/ 会议室列表（restframework 纯接口）
    http://0.0.0.0:8000/meeting/meeting/ 会议列表（restframework 纯接口）
    http://0.0.0.0:8000/doc/ 查看接口文档

# 一些说明

目前市面公司一般采取前后端分离的开发方式，程序员的技能栈前后端也不相同。
本程序中, admin.py form.py 是纯用于django管理后台开发而编写的代码。
正常是类似views中继承rest_framework的viewset来写接口及方法。
之所以开发了django管理后台，是因为1有界面可看 2django管理后台的开发方式和某些低代码框架开发方式很相似。
两套都是尽可能追求框架最佳实践的代码。

# 开发规范
    
参考文档：
django 官方文档：https://docs.djangoproject.com/en/4.1/
django rest framework 官方文档：https://www.django-rest-framework.org/api-guide/viewsets/

样例参考meeting模块。

### 分层：
    
    models
    migrations
    views
    serializers
    urls
    tests
    
    admin (管理后台)
    apps (管理后台)
    form (管理后台)

### models:
    
    加好索引
    业务逻辑方法（剥离权限与展示相关）放在此处

### views:
    
    url viewset 增删改查 + actions
    
    如果viewset不需要删除 可以不直接继承ModelViewset
    
    


#### 权限
    
    对django管理后台开发来说，权限是饱受诟病的缺陷之一。
    在本程序中我举了一个例子：用户只能编辑自己新建的会议，这样一个简单业务功能
    如restframework的开发模式，并不难实现，在django form 管理后台，改出来这个权限的成本相当高。
    当然restframework权限开发模式方式也有缺陷，简单的权限管理，消耗了多行代码，完全可以简化。
    这块我的最佳实践是使用casbin管理权限语句，基于casbin权限模型，可以实现rbac abac 域隔离 等任意权限方案（https://casbin.org/ 参考casbin相关权限模型论文）。
    相关代码不在手无法参考。。。先简单跑通吧。


#### 其它说明 django项目两种开发方式和低代码相关的一些思考 
    
    同时进行了django管理后台开发和restframework的开发。
    可以看到，管理后台功能十分强大，以极少量的代码快速形成了前端界面。并支持大量常规功能，crud，操作日志，权限，等等。
    某种意义上可以说，将django管理后台的开发前端化，即形成了一个简单版的，通用低代码框架。

    但是缺陷也很多：在要增加自定义api如启用停用会议室，以及对api进行业务优化提升如加锁时，很明显不如restframework的开发方式。
    管理后台这些难于使用的点，导致其在市场上几乎难觅其踪，公司略成熟点几乎都会另行重做。
    且前后分离是大势所趋，事实上目前市场环境前后端在人员技能上就分离开了。需要以接口规范重新接通前后端，而不能做成代码层面耦合。

    相应地，即便不比较界面功能，restframework viewset的开发方式，在权限、操作日志、代码序列化等多个功能点，仍弱于django管理后台。
    框架落后，造成后端无谓的工作量，以及开发难度增大。
    如若提供合理的低代码结构，可以使后端开发更为容易，甚至达到产品经理可用的水平。并能进行良好的前后端分离。
    我之前以flask框架开发了流程引擎，很多思路是来自于此，利用前端界面制作类似django管理后台程序的标准代码。

    以上即完成了我期望的流程引擎的可变表单部分。
    再加bpmn流程图和流程节点相关功能，将可变表单链接起来，或许就可走向我期望的流程引擎平台最终形态。
    如果固化bpmn流程图，固化特定的流程节点类型，即可形成特定行业内的特定流程平台，以通用性下降换取了开发时效。


#### todos

作为一个模块最佳实践案例，目前该项目尚缺：

    1、单元测试 unittest方法级 或 django test api级测试
    2、自动化测试 编写测试用例，基于webapitest自动化测试 实现双向review
    3、权限开发和配置：基于casbin的最佳权限实践
    4、模块开发常规流程的一些说明、模块设计相关图文叙述
    5、部署相关 docker，jenkins持续集成等
    6、配置简化相关
    7、性能相关
    8、国际化相关
