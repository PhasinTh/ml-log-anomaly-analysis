# Detecting Malicious Log in Access Log
ภัยคุกคามของระบบเครือข่ายมาจากการที่ฮาร์ดแวร์หรือซอฟต์แวร์ใช้งานไม่ได้ หรือการโจมตีจากผู้ไม่ประสงค์ดี การเก็บล็อกกิจกรรมบนเครือข่าย (Network logs) เพื่อตรวจสอบสิ่งที่เกิดขึ้น เป็นรูปแบบหนึ่งของการป้องกันต่อความล้มเหลวของระบบและการโจมตีของมนุษย์ บ่อยครั้งที่แอปพลิเคชันบนเว็บเผชิญกับกิจกรรมที่น่าสงสัยเนื่องจากสาเหตุต่าง ๆ เช่น การสแกนเว็บไซต์โดยใช้เครื่องมือสแกนช่องโหว่อัตโนมัติ หรือมีผู้ที่พยายามส่งพารามิเตอร์สำหรับการทำ SQL injection ซึ่งในหลาย ๆ กรณี ล็อกบนเว็บเซิร์ฟเวอร์จะใช้วิเคราะห์เพื่อหาว่าเกิดอะไรขึ้น หากเป็นกรณีที่ร้ายแรงอาจต้องทำการตรวจสอบทางนิติวิทยาศาสตร์ (Forensics) เครือข่ายขนาดกลางถึงขนาดใหญ่มีกิจกรรมเครือข่ายปริมาณมาก สร้างไฟล์บันทึกขนาดใหญ่ ซึ่งทำให้การตรวจสอบด้วยคนนั้นเป็นได้ยาก โปรเจคการพัฒนาโปรแกรมตรวจจับการโจมตีจากบันทึกการเข้าการเข้าถึง (access logs) วัตถุประสงค์เพื่อการรุกล้ำที่เกิดบนเว็บแอปพลิเคชัน และวิเคราะห์การโจมตีจากบันทึกการเข้าการเข้าถึง (access logs) โดยการใช้งานอัลกอริทึมแรนดอมฟอเรสต์ (Random Forest) และตรวจจับการโจมตีประเภท SQL injection, Cross Site Scripting และ Directory Traversal

## โครงสร้างโปรแกรม
<img src="https://i.imgur.com/3f2pSHa.png">

## การตรวจจับเอกลักษณ์และการตรวจความผิดปกติ (Signature detection and Anomaly detection)
- Signature detection คือการตรวจจับโดยการค้นหาเอกลักษณ์ (Signature) ง่ายต่อการพัฒนาและเข้าใจ ทำงานได้ดีกับการโจมตีด้วยรูปแบบพฤติกรรมคงที่ไม่สามารถทำงานได้ดีกับ รูปแบบการโจมตีจำนวนมาก ที่สร้างขึ้นโดยมนุษย์หรือเวิร์มที่มีลักษณะพฤติกรรมที่ปรับเปลี่ยนได้เอง 
- Anomaly detection คือการตรวจจับพฤติกรรมที่ต่างไปจากปกติ เรียนรู้หรือระบุโดยผู้ดูแลระบบเครือข่ายหรือทั้งสองอย่าง ความผิดปกตินั้นเกิดจากพฤติกรรมใด ๆ ที่อยู่นอกรูปแบบพฤติกรรมที่กำหนดไว้ล่วงหน้าหรือเป็นที่ยอมรับ

## กระบวนรวบรวมข้อมูล
กระบวนรวบรวมล็อกเพื่อนำมาใช้ให้กับการเรียนรู้ของเครื่องนั้น ผู้วิจัยได้รวบรวมล็อกจากแหล่งเผยเพร่ที่เป็นสาธารณะจากเว็บไซต์ Kaggle และล็อกของNASA และใช้วิธีสร้างล็อกที่เป็นล็อกที่เป็นการโจมตีขึ้นมา โดยมีขั้นตอนดังนี้
ติดตั้งเซิร์ฟเวอร์ที่มีช่องโหว่ Damn Vulnerability Web Application (DVWA) เพื่อใช้เป็น
ใช้เครื่องมือสแกนช่องโหว่อัตโนมัติ โดยใช้เครื่องมือ Nikto, Grabber, OWASP zed attack proxy project
Nikto ใช้ในการตรวจสอบไฟล์หรือพาทที่ไม่ปลอดภัย ในระบบสแกนหาช่องโหว่เว็บไซต์ ซึ่งเป็นช่องทางที่ผู้ไม่ประสงค์ดีใช้ในการโจมตีเว็บไซต์ได้
Grabber เป็นเครื่องมือสแกนช่องโหว่บนเว็บไซต์ ได้รับการออกแบบมาสำหรับใช้กับเว็บไซต์ขนาดเล็ก อย่างเว็บไซต์ส่วนตัวหรือฟอรั่ม
OWASP zed attack proxy project เป็นเครื่องมือสแกนหาช่องโหว่บนเว็บไซต์ สามารถใช้เพื่อหาช่องโหว่บนเว็บไซต์ที่สร้างขึ้นเอง หรือใช้สำหรับการฝึกฝีมือของนักเจาะระบบ

## การเตรียมข้อมูลและการสกัดคุณลักษณะ
การเตรียมข้อมูลก่อนนำไปใช้สามารถทำขั้นตอนด้านล่างนี้ได้
- Parsing ข้อมูล แบ่งล็อกแต่ละแถวออกเป็นส่วน ๆ เพื่อใช้ในขั้นตอนการคัดเลือกฟีเจอร์
- จำแนกคลาสการโจมตี แล้วติดเลเบลให้กับข้อมูล ดังนี้
	- แทน N กับล็อกที่เป็นปกติ 
 	- แทน XSS กับล็อกที่เป็นการโจมตีแบบ XSS 
	- แทน SQLi กับล็อกที่เป็นการโจมตีแบบ SQL Injection 
	- แทน DT กับล็อกที่เป็นการโจมตีแบบ Directory Traversal
- เลือกฟีเจอร์ที่มีความสัมพันธ์กับผลลัพธ์ คลาสคำตอบ

## ฝึกสอนโมเดล (Training Model)
<p>เทคนิคที่นำมาใช้ในการทดลองพัฒนาตัวแบบมีทั้งหมด 5 เทคนิค ซึ่งผู้วิจัยได้ใช้ไลบรารีจาก sklearn ได้แก่ svm (Support Vector Machine), GaussianNB (Naive Bayes), KNeighborsClassifier (K Nearest Neighbors), DecisionTreeClassifier (Decisionไป Tree) และ RandomForestClassifier (Random Forest) </p>
<p>การฝึกสอนโมเดล กระทำโดยเริ่มจากการนำข้อมูลที่เตรียมไว้ มาแบ่งในอัตราส่วน 7 ต่อ 3 โดย 7 ส่วนนี้ใช้ในการสอนโมเดลให้เรียนรู้ทั้งอินพุตและเอาต์พุต (class) และอีก 3 ส่วนจะใช้ในการทดสอบโมเดล ใช้ ไลบรารีใน sklearn ชื่อ train_test_split</p>
<p>ค่าวัดประสิทธิภาพตัวแบบที่ผู้วิจัยจะให้ความสำคัญ คือ ค่าความระลึก (Recall) เป็นหลัก เนื่องจากงานวิจัยนี้เป็นการพัฒนาโมเดลเพื่อใช้ในการตรวจจับล็อกที่เป็นการโจมตีซึ่งค่า ความระลึก (Recall) จะเป็นค่าที่แสดงให้เห็นถึงความสามารถในการทำนายของโมเดลว่าสามารถทำนายได้ครอบคลุมเพียงใด</p>

## วัดประเมินประสิทธิภาพของโมเดล
<img src="https://i.imgur.com/YxjJkbE.png">
<p>ค่าวัดประสิทธิภาพที่ผู้วิจัยจะให้ความสำคัญ คือ Recall เป็นหลัก เนื่องจากงานวิจัยนี้เป็นการพัฒนาโมเดลเพื่อใช้ในการตรวจจับล็อกที่เป็นการโจมตีซึ่งค่า ความระลึก (Recall) จะเป็นค่าที่แสดงให้เห็นถึงความสามารถในการทำนายของโมเดลว่าสามารถทำนายได้ครอบคลุมเพียงใด</p>
<p>จากตารางวัดผลข้างบนจะแสดงให้เห็นว่าอัลกอริทึมแรนดอมฟอเรสต์ มี Recall สูงกว่าอัลกอริทึมอื่น ทางผู้จัดทำจึงได้นำโมเดลของอัลกอริทึมแรนดอมฟอเรสต์มาใช้ในแอปพลิเคชันเพื่อแสดงผลการตรวจจับล็อกที่เป็นการโจมตี</p>

## หน้าผู้ใช้งาน (User Interface) และ การนำเสนอข้อมูล (Data Visualization)
* หน้าผู้ใช้งานหน้าแรกสุดจะเป็นการนำเข้าไฟล์ล็อกจากเครื่องผู้ใช้งาน <img src="https://i.imgur.com/KHT0t10.png">
* จากนั้นแอปพลิเคชันจะทำการอัปโหลดและประมวลผลล็อกเมื่อเสร็จแล้วจะทำการเปลี่ยนหน้าไปที่หน้าแสดงผล โดย
	* **ส่วนแรก** แสดงรายระเอียดข้อมูลของไฟล์ ข้อมูลล็อก และ จำนวนล็อคการโจมตีที่พบ 
	* **ส่วนที่สอง** กราฟวงกลมแสดงอัตราส่วนของการโจมตีแต่ละประเภทที่ตรวจจับได้ เทียบกับเฉพาะการโจมตีทั้งหมด <img src="https://i.imgur.com/RvXFSID.png">
	* **ส่วนที่สาม** แสดง 10 อันดับไอพีที่มีจำนวนการโจมตีสูงที่สุด และเมื่อทำการคลิกไปที่ไอพี จะแสดงรายละเอียดล็อกที่ผิดปกติจากไอพีนั้นทั้งหมด <img src="https://i.imgur.com/CtVHK4W.png">
	* **ส่วนที่สี่** ข้อมูลล็อกทั้งหมดโดยจะมีรายละเอียดต่าง ๆ รวมถึงเลขแถวของเรคคอร์ด พร้อมระบุประเภทการโจมตีส่วนนี้สามารถค้นหาข้อมูลที่สนใจ ฟิลเตอร์ให้แสดงเฉพาะล็อกที่ตรวจจับเท่านั้น เปิดปิดตัวไฮไลท์ และสามารถส่งออกข้อมูลล็อกเป็นไฟล์ csv เพื่อนำไปใช้งานต่อได้ <img src="https://i.imgur.com/jqoBGLc.png">


## Technology
### Rest Api

The Api is served using a Flask blueprint at `/api/` using Flask RestPlus class-based
resource routing.

### Client Application

A Flask view is used to serve the `index.html` as an entry point into the Vue app at the endpoint `/`.

The template uses vue-cli 3 and assumes Vue Cli & Webpack will manage front-end resources and assets, so it does overwrite template delimiter.

The Vue instance is preconfigured with Filters, Vue-Router, Vuex; each of these can easilly removed if they are not desired.

### Important Files

| Location             |  Content                                   |
|----------------------|--------------------------------------------|
| `/app`               | Flask Application                          |
| `/app/api`           | Flask Rest Api (`/api`)                    |
| `/app/client.py`     | Flask Client (`/`)                         |
| `/src`               | Vue App .                                  |
| `/src/main.js`       | JS Application Entry Point                 |
| `/public/index.html` | Html Application Entry Point (`/`)         |
| `/public/static`     | Static Assets                              |
| `/dist/`             | Bundled Assets Output (generated at `yarn build` |
| `/models/`           | Machine Learning Models                    |


## Installation

### Before you start

Before getting started, you should have the following installed and running:

- [X] Yarn - [instructions](https://yarnpkg.com/en/docs/install#mac-stable)
- [X] Vue Cli 3 - [instructions](https://cli.vuejs.org/guide/installation.html)
- [X] Python 3
- [X] Pipenv (optional)
- [X] Heroku Cli (if deploying to Heroku)

### Template and Dependencies
* Setup virtual environment, install dependencies, and activate it:

	```
	$ pipenv install --dev
	$ pipenv shell
	```

* Install JS dependencies

	```
	$ yarn install
	```

## Development Server

Run Flask Api development server:

```
$ python run.py
```

From another tab in the same directory, start the webpack dev server:

```
$ yarn serve
```

The Vuejs application will be served from `localhost:8080` and the Flask Api
and static files will be served from `localhost:5000`.

The dual dev-server setup allows you to take advantage of
webpack's development server with hot module replacement.

Proxy config in `vue.config.js` is used to route the requests
back to Flask's Api on port 5000.

If you would rather run a single dev server, you can run Flask's
development server only on `:5000`, but you have to build build the Vue app first
and the page will not reload on changes.

```
$ yarn build
$ python run.py
```

## Production with Docker
* Install dependencies and Build Vue production:

	yarn
	```
	$ yarn install
	$ yarn run build
	```

	npm
	```
	$ npm install
	$ npm run build
	```

* Build:

	```
	$ docker build -t malicious-log-detect .
	```

* Deploy:

	```
	$ docker run -p 80:5000 malicious-log-detect
	```

## Production Server

This template is configured to work with Heroku + Gunicorn and it's pre-configured
to have Heroku build the application before releasing it.

### JS Build Process

Heroku's nodejs buidlpack will handle install for all the dependencies from the `packages.json` file.
It will then trigger the `postinstall` command which calls `yarn build`.
This will create the bundled `dist` folder which will be served by whitenoise.

### Python Build Process

The python buildpack will detect the `Pipfile` and install all the python dependencies.

### Production Sever Setup

Here are the commands we need to run to get things setup on the Heroku side:

	```
	$ heroku apps:create malicious-log-detect
	$ heroku git:remote --app malicious-log-detect
	$ heroku buildpacks:add --index 1 heroku/nodejs
	$ heroku buildpacks:add --index 2 heroku/python
	$ heroku config:set FLASK_ENV=production
	$ heroku config:set FLASK_SECRET=SuperSecretKey

	$ git push heroku
	```

### Heroku deployment - One Click Deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/gtalarico/flask-vuejs-template)
