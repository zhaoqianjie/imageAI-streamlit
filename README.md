# balloon

## Streamlit是一个开源库，可以帮助数据科学家和学者在短时间内开发机器学习 (ML) 可视化仪表板。只需几行代码，我们就可以构建并部署强大的数据应用程序

## 优点：使用python开发前端，可以方便的构建图表进行展示
## 缺点：内部封装了CSS样式，样式改动困难，甚至不能改动。对比vue等前端框架用户交互能力更弱。

## 项目目录
/  
|-- .streamlit  (配置文件)  
|-- streamlit_gallery  (项目主体文件)  
|---- readme (readme页面)  
|---- routers (项目路由)  
|------ object_detection (目标识别模块路由)  
|---- utils (工具函数)  
|---- views (视图文件夹)  
|------ object_detection (目标识别视图文件夹)  
|------ status_code (状态码)  
|------ text_collector (文本管理)  
|-- app.py (项目入口文件)


## 启动
## streamlit run app.py
