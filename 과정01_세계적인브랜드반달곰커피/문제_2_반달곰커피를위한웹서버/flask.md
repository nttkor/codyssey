## Flask Tutorial Links Update
- [Flask 강의 1 - 생활코딩](https://opentutorials.org/course/4904)
- [Flask 강의 2 - Easy IT Wanner 블로그](https://easyitwanner.tistory.com/347)

## 앱 팩토리와 블루 프린트
###  목차
- 플라스크 앱 팩토리(Flask Application Factory)
- 블루 프린트(Blue print)
- 예시

#### 플라스크 앱 팩토리
Flask 애플리케이션 팩토리(Application Factory)는 유연성을 제공하고 우수한 애플리케이션 설계를 촉진하는 방식으로 애플리케이션을 구조화하기 위해 Flask가 권장하는 디자인 패턴입니다. 
애플리케이션 팩토리의 기본 개념은 앱을 설정하기 위해 호출할 수 있는 함수(일반적으로 create_app()라는 이름)로 Flask 애플리케이션을 생성하는 것입니다. 
이를 통해 서로 다른 설정으로 동일한 애플리케이션의 여러 인스턴스를 만들 수 있습니다.

다음은 애플리케이션 팩토리가 어떻게 보이는지 보여주는 예시입니다.
## Flask 앱 팩토리 패턴 예제

```python
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 여기서 확장을 초기화합니다...
    # 예: db.init_app(app), login_manager.init_app(app) 등

    # 여기에 블루프린트 등록...
    # 예: from .views import main as main_blueprint
    #     app.register_blueprint(main_blueprint)

    return app
```
이 예제에서 config_name은 Flask 애플리케이션의 구성을 결정하는 데 사용되며, 이를 통해 개발, 테스트 및 프로덕션과 같은 환경마다 다른 구성을 사용할 수 있습니다. Flask 애플리케이션을 시작하려면 다음과 같이 하면 됩니다.
```python
from your_flask_package import create_app

app = create_app('development')

if __name__ == "__main__":
    app.run()
        ```
이 패턴의 장점은 다음과 같습니다.

테스트: 다양한 설정으로 애플리케이션의 테스트 인스턴스를 생성하여 제대로 테스트할 수 있습니다.
여러 인스턴스: 동일한 프로세스에서 동일한 애플리케이션의 인스턴스를 여러 개 생성할 수 있습니다.
블루프린트: 애플리케이션 팩토리에 블루프린트를 등록할 수 있으므로 애플리케이션 디자인에 블루프린트 및 모듈성을 사용할 수 있습니다.
확장: 애플리케이션 팩토리에서 확장을 초기화할 수도 있습니다.


#### 블루 프린트(Blue print)
Flask의 블루프린트는 관련 경로, 오류 처리기 및 기타 HTTP 관련 기능을 재사용 가능한 별도의 Python 모듈로 그룹화하는 방법입니다. 애플리케이션이 복잡해질 때 특히 유용할 수 있습니다. 블루프린트를 만드는 방법은 다음과 같습니다.
```python
from flask import Blueprint

my_blueprint = Blueprint('my_blueprint', __name__)

@my_blueprint.route('/hello')
def hello():
    return 'Hello, World!'
```
이 예제에서는 'my_blueprint'라는 이름의 새 블루프린트를 생성합니다. 그런 다음 해당 블루프린트에 경로를 정의합니다. 이 블루프린트를 플라스크 애플리케이션에 등록하면 애플리케이션의 일부로 경로를 사용할 수 있습니다. 블루프린트에는 여러 가지 기능이 있으며 몇 가지 다른 방식으로 사용할 수 있습니다.

1. URL 접두사블루프린트를 등록할 때 URL 접두사를 제공할 수 있습니다. 블루프린트에 정의된 모든 경로에는 이 접두사가 붙습니다. 관련 경로를 함께 그룹화할 때 유용합니다. 
app.register_blueprint(my_blueprint, url_prefix='/prefix')
이 경우 앞서 정의한 '/hello' 경로는 실제로 애플리케이션에서 '/prefix/hello'에 위치하게 됩니다. 

2. 하위 도메인마찬가지로 블루프린트를 등록할 때 하위 도메인을 지정할 수도 있습니다. 그러면 블루프린트의 모든 경로를 해당 하위 도메인에서 사용할 수 있습니다. 

3. 애플리케이션 전체 에러 핸들러블루프린트는 애플리케이션에서 오류 처리기를 정의하는 방법과 유사하게 오류 처리기를 정의할 수 있습니다. 블루프린트에 오류 처리기가 정의되어 있으면 해당 블루프린트에 정의된 경로에서 요청을 처리할 때 발생하는 오류에 사용됩니다. 

4. 요청 전/요청 후/해체 요청 핸들러에러 핸들러와 마찬가지로 블루프린트에도 이러한 특수한 유형의 핸들러를 정의할 수 있습니다. 

5. 템플릿 및 스태틱 파일블루프린트에는 자체 템플릿과 스태틱 파일이 있을 수 있으며, 애플리케이션의 특정 부분과 관련된 리소스를 구성하는 데 유용할 수 있습니다.

#### 예시
애플리케이션 팩토리와 블루프린트를 모두 사용하는 플라스크 애플리케이션의 예를 살펴보겠습니다. 간단히 설명하기 위해 누구나 글을 볼 수 있는 공개 영역과 권한이 있는 사용자가 글을 작성하고 편집할 수 있는 관리자 영역의 두 가지 주요 부분으로 구성된 기본 블로그 애플리케이션을 만들어 보겠습니다. 프로젝트의 디렉토리 구조는 다음과 같습니다.
```
/Learning
    /blogapp
        /admin
            __init__.py
            views.py
        /public
            __init__.py
            views.py
        __init__.py
        config.py
    main.py
``` 
각 부분을 살펴봅시다.
1. blogapp/admin/views.py 및 blogapp/public/views.py이 모듈은 각각 애플리케이션의 관리자 및 공개 부분에 대한 뷰를 정의합니다. 이 모듈은 각각 청사진을 생성하고 해당 청사진에 대한 경로를 정의합니다.

# blogapp/admin/views.py
```python
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def index():
    return "관리자 구역에 오신 것을 환영합니다!"
    ``` 
# blogapp/public/views.py
```python
from flask import Blueprint

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    return "퍼블릭 구역에 오신 것을 환영합니다!"
``` 
2. blogapp/admin/__init__.py 및 blogapp/public/__init__.py이 모듈은 애플리케이션을 만들 때 사용할 수 있도록 블루프린트를 가져옵니다.
# blogapp/admin/__init__.py
```python
from .views import admin_bp
# blogapp/public/__init__.py
from .views import public_bp
``` 
3. blogapp/config.py이 모듈은 애플리케이션의 다양한 구성을 정의합니다. 간단하게 하기 위해 하나의 기본 구성만 정의하겠습니다. 
# blogapp/config.py
```python
class Config:
    SECRET_KEY = 'supersecretkey'
``` 
4. blogapp/__init__.py이 모듈은 애플리케이션 팩토리를 정의합니다. 이 모듈은 새로운 Flask 애플리케이션을 생성하고, 구성을 로드하고, 블루프린트를 등록합니다.
# blogapp/__init__.py
```python
from flask import Flask

from .config import Config
from .public import public_bp
from .admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)
    
    return app
``` 
5. main.py: 이것이 애플리케이션의 진입점입니다. 애플리케이션 팩토리를 가져와서 애플리케이션의 새 인스턴스를 생성하는 데 사용합니다. 
# main.py
```python
from blogapp import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
```
 
이렇게 구성을 마치고 나면 다음과 같이 파일이 구성되야 합니다.

예시 구성 요소 설명

Blueprint블루프린트는 관련 라우트, 오류 처리기 및 기타 HTTP 관련 함수 그룹을 Python 모듈로 구성하는 방법입니다. 이를 통해 애플리케이션 기능을 논리적 단위로 분리할 수 있으므로 애플리케이션이 커질수록 관리하기가 더 쉬워집니다. 

create_app()애플리케이션 팩토리 함수입니다. 이 함수는 플라스크 애플리케이션의 인스턴스를 생성하고, 구성하고, 블루프린트를 등록하는 역할을 합니다. 애플리케이션 팩토리는 서로 다른 구성으로 애플리케이션의 여러 인스턴스를 생성할 수 있기 때문에 유용한 디자인 패턴이며, 특히 테스트에 유용할 수 있습니다. 

ConfigConfig 클래스는 플라스크 애플리케이션의 구성 변수를 저장하는 데 사용됩니다. 이러한 변수에는 데이터베이스 URI, 세션 쿠키의 비밀 키 등이 포함될 수 있습니다. 주어진 예제에서는 Flask가 쿠키 서명과 같은 작업에 사용하는 SECRET_KEY 구성이 정의되어 있습니다. 

app.config.from_object(Config)이 줄은 Config 클래스의 구성을 Flask 애플리케이션으로 로드합니다. Flask는 구성 변수를 로드하는 여러 가지 방법을 제공하며, from_object()는 그 중 하나로 파이썬 객체에서 구성 변수를 로드할 수 있게 해줍니다. 

app.register_blueprint()이 메서드는 플라스크 애플리케이션에 블루프린트를 등록하는 데 사용됩니다. 블루프린트가 등록되면 모든 경로와 에러 핸들러가 애플리케이션의 일부가 됩니다. 
url_prefix='/admin'블루프린트를 등록할 때 URL 접두사를 제공할 수 있습니다. 

해당 블루프린트에 정의된 모든 경로에는 이 URL 접두사가 붙습니다. 이 예제에서는 관리자 청사진의 모든 경로가 '/admin' 아래에 있습니다. 

if __name__ == '__main__': app.run()이것은 직접 실행하려는 스크립트에 대한 일반적인 파이썬 관용구입니다. 이 스크립트가 직접 실행되는 경우(예: 명령줄에 python main.py를 입력하여) __name__은 '__main__'이 되고 Flask 애플리케이션이 시작됩니다. 이 스크립트를 다른 스크립트에서 모듈로 가져온 경우 __name__은 'main'이 되고 Flask 애플리케이션은 시작되지 않습니다. 이렇게 하면 Flask 애플리케이션을 시작하지 않고도 이 스크립트의 함수와 클래스를 재사용할 수 있습니다.

실행
여기서는 Learning 디렉토리에서 main을 플라스로 작동시키기 위해 다음 명령어를 입력해줍니다.
# 실행할 디렉토리 경로
# D:\Working_Files\07_Python-Project\Projects\Project_01\Learning
# 위 경로는 자신의 경로에 맞겍 지정해주세요

set FLASK_APP=main
 
다음 이미지와 같이 주소에 해당 /admin을 추가하면 다른 화면으로 이동할 수 있습니다.

버튼을 만들어서 이동하거나 할 수 있지만 이는 나중에 더 다뤄보도록 하겠습니다. 이번 포스팅은 여기서 마칠게요~
출처: https://easyitwanner.tistory.com/351 [IT 시작해보기:티스토리]