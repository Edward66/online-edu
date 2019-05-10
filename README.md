# online-edu

使用python2.7 + django1.09打造的在线教育平台，项目完成后升级到python3.6+django2.22。



## 使用
```python
git clone https://github.com/Edward66/online-edu.git
cd Mxonline3
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


## 关于虚拟环境
```python
# 安装
pip install virtualenv
pip install virtualenvwrapper

# 修改.zshrc（oh-my-zsh用户）或.bashrc
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

#创建
mkvirtualenv online-edu -p 'python3.6'
```