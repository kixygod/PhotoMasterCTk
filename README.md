# Photo Master

<p align="center">
  <img width="500" src="/screenshots/dark.png">
  <img width="500" src="/screenshots/light.png">
</p>
Данное приложение было разработано на языке Python с помощью библиотеки Custom Tkinter. Основная задача данного приложения быстрое и простое редактирование базовых параметров любого изображения.
Руководство использования:

1. Перейдите во вкладку 'Edit photo';
2. Далее нажмите на кнопку в правом верхнем углу 'Upload photo';
3. После этого вам будет доступно редактирование базовых параметров вашего изображения

Данное приложение было разработано для учебы, в частности для предмета 'Объектно-ориентированнео программирование'

## How to run

```bash
cd PhotoMasterCTk
pip install virtualenv
.\env\Scripts\activate
pip install -r .\requirements.txt
python -u .\app.py
```

Чтобы использовать тесты

```bash
python -m unittest .\test_app.py
```
