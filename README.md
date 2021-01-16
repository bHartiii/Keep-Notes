# Keep-Notes

**Description** : 
- This is django Project in which rest APIs are created for authentication and notes creation.
- There are two apps in this project : 
    * authentication
    * notes
- **authentication** app provides APIs for following features:
    * Registration using email verification.
    * Login and logout
    * Reset password
    * UserProfile 
- For authentication JWT token is used. 
- For user profile creation signal is used.

- **notes** app provides APIs for following features :
    * Create and list notes
    * Create and list labels
    * Archive note
    * Trash note
    * Update note 
    * Update label
    * Delete note
    * Delete label
    * Retrieve Note
    * Retrieve label
    * List all archived notes
    * List all trashed notes
    * Add labels to a note

- **JWT Token :** JWT is an encoded JSON string that is passed in headers to authenticate requests. It is usually obtained by hashing JSON data with a secret key. This means that the server doesn't need to query the database every time to retrieve the user associated with a given token.  

- **The Concept of Authentication and Authorization:**  
Authentication is the process of identifying a logged-in user, while authorization is the process of identifying if a certain user has the right to access a web resource.

- **Signals** : Django includes a “signal dispatcher” which helps allow decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place. They’re especially useful when many pieces of code may be interested in the same events.

- **Celery:** We can call a celery task by two ways:
    - Synchronous : The method is exceuted in same thrad.
    - Asynchronous : The message is sent to celery worker by using rabbitMQ server.
    Ex : method_name.delay() : It create json message and paass it to celery worker.
    - Celery uses rabbitMQ serve as message broker that passes the message from django to celery worker.
    - By using status property we can check status of asychronous tasks.


### Django Project Creation :

#### Project setup and database structure:
- start the project by creating and entering the folder KeepNotes.
    1. mkdir KeepNotes 
    2. cd KeepNotes

- Create a virtual environment.
    1. For windows : python -m venv keep

- Activate the virtual environment.
    1. keep/Script/activate

- Install **Requirements** of this project:
    1. pip install django
    2. pip install djangorestframework
    3. pip install django-rest-framework jwt
    4. pip install pyshortners
    5. pip install django-redis
    6. pip imstall celery
    7. pip install django-celery-results
    8. pip install django-celery-beat

- create our project using a command-line utility provided by django.
    1. django-admin startproject KeepNotes


### Start the project:

- Use this command to start server : python3 rest/manage.py runserver
- It might give the warning regarding migrations, for now, ignore it. The screen must look like this :  

      Watching for file changes with StatReloader
      Performing system checks...
      System check identified no issues (0 silenced).
      You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
      Run 'python manage.py migrate' to apply them.
      December 18, 2019 - 05:46:38
      Django version 2.2.5, using settings 'rest.settings'
      Starting development server at http://127.0.0.1:8000/
      Quit the server with CONTROL-C.


- Hit http://127.0.0.1:8000/ and you would see the following:

![alt text](https://miro.medium.com/max/1024/1*iUYrqXey05CBs-ckc1a68Q.png)


### Database connection with project:

- In settings.py file :
    1. For mongodb :  

            DATABASES = {
                'default': {
                    'ENGINE': 'djongo',
                    'NAME': 'database_name',
                }
            }

    2. For Postgres :
      
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': 'database name',
                    'USER': 'postgres',
                    'PASSWORD': 'password',
                    'PORT': '5432',
                }
            }


### Create App:

- python manage.py startapp app_name
- cd app_name
    ( In this case app name is authentication  )
- Configuration of routes:
    * Create file in urls.py inside app.
    * Inside project root directory add the path of this created urls.py in app :  

            path('auth/',include('authentication.urls'))

    * Inside app in the urls.py file add route for view created in app.

- Repeat these steps for notes app.

### Create Models For App:

- In Django models are used to define the database layout or in simple terms tables in the database.
- There are two models in authentication app:
    1. User
    2. UserProfile
- There are two models in notes app:
    1. Notes
    2. Labels

- **User Model :** 
    - Create a custom user manager by extending BaseUserManager and providing two additional methods:
        * create_user() and create_superuser()
        * create_user() and create_superuser() must accept username field and other required fields as args:   
            1. Inside create_user():

                - self.normalize_email(email) normalizes the email address by lowercasing the domain part.
                - set_password(password) stores the password and saves the hash in the database.
                - user.save(using=self._db) saves the user in the current database (self._db)
                - finally, this method returns the user if saved successfully else throws an error.

            2. create_superuser() saves the user with admin permissions which are achieved by enabling is_superuser = True and is_staff = True.

    - class User extends AbstractBaseUser to create a user with custom fields:
        * USERNAME_FIELD is set to email as it should be used as username while login.
        * REQUIRED_FIELDS contain a list of fields required but in our case it’s empty.

- **UserProfile :** 
    - Create a image field in user profile model. 
    - There is one to one relation between user and profile.

- **Notes Model :**
    * Create field notes information like name, owner, date etc.
    * For owner there is a manyToOne relation with User model.
    * Create manyTomany relation between notes and labels:

            owner=models.ForeignKey(to=User, on_delete=models.CASCADE)
            label = models.ManyToManyField(to=Labels)

- **Labels Model:**
    * There is owner field also like notes.

- Custom AUTH_USER_MODEL setting:
    By default, Django assumes that the user model is django.contrib.auth.models.User. We want to use our own custom User though. Since we've created the User class, the next thing we need to do is to tell Django to use our User model instead of using its own.
    1. AUTH_USER_MODEL = 'authentication.User'


### Register app and models:

- Register app in settings.py:

        INSTALLED_APPS = [    
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'authentication.apps.AuthenticationConfig',
            'notes',
        ]


- Register models in admins.py:
    * authentication app:

            from django.contrib import admin
            from authentication.models import User, UserProfile
            admin.site.register(User)
            admin.site.register(UserProfile)

    * notes app :
        Like authentication app for notes app also models need to be registered in admins.py

### Storing uploaded pictures:

- Create media folder in project root directory.
- in image field of user rpofile specify the path of image inside media.
- In settings:
        
            MEDIA_URL = '/media/'
            MEDIA_ROOT = 'media'

- In project;s urls add the following to urlpatterns list so that images can be accessed by url:

            +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


### Migration:

* Django provides us with the command-line utility to handle migrations.
    - migrate : python manage.py makemigrations
    - makemigrations : python manage.py migrate

            python manage.py makemigrations  KeepNotes/authentication/profile/migrations/0001_initial.py #output
            - Create model User
            - Create model UserProfile
            - Create model Notes
            - Create model Labels
            python manage.py migrate
            Operations to perform:   #output
            Apply all migrations: admin, auth, contenttypes, userprofile, sessions, user, notes, labels
            Running migrations:
                Applying user.0001_initial... OK
                Applying userprofile.0001_initial... OK
                Applying notes.0001_initial... OK
                Applying labels.0001_initial... OK


### Create user profile using signals:

- Create a file signals.py in app.
- user post_save() and create a receiver funaction : 

        @receiver(post_save,sender=User)
        def create_user_profile(sender, instance, created, **kwargs):
            if created:
                UserProfile.objects.create(user=instance)

- Register signals by re writing ready() in apps.py
            
        def ready(self):
            import authentication.signals


### Storing and retrieving the data in JSON:

- **Serializers** : Serializer storing and retrieving the data in JSON as the response we want from our API is in JSON.
                It allows complex data and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types.

- To creaet serializer create a class that extends the serializers class of restframework.
- Every serializer contains meta class inside model is set and fields of models are also given.
- To perform validations on request data there is a validate(). It performs validations and raises exception if any occurs. 
- Tells the fields to be used by the serializer. If we want to include all the fields of the model then we can simply use.
    fields = ('__all__')

        class RegisterSerializer(serializers.ModelSerializer):
        password = serializers.CharField(max_length=68,  min_length=6, write_only=True, style={'input_type': 'password'})

        class Meta:
            model=User
            fields = ['email', 'username', 'password']

        def validate(self, attrs):
            email = attrs.get('email','')
            username = attrs.get('username','')
            if not username.isalnum():
                raise serializers.ValidationError('Username should contain alphanumeric values only')
            return attrs

        def create(self, validate_data):
            return User.objects.create_user(**validate_data)


- Create serializers.py file inside the authentication app and create following serializer for every view in the views.py:
    1. RegisterSerializer
    2. EmailVerificationSerializer
    3. LoginSerilaizer
    4. ResetPasswordSerializer
    5. NewPasswordSerializer
    6. UserProfilrSerializer

- Create following serializer for notes app:
    1. NotesSerializer
    2. LabelsSerializer
    3. ArchiveNotesSerializer
    4. TrashSerializer
    5. AddNotesInLabelsSerializer
    6. AddLabelsToNoteSerializer


### Create views for authentication:

- Create the endpoint for registering the user by creating views.py file under user.
- All views are class based and inherit generic views.
- In every view class permission and serialzer_class has to be set.
- For permissions add these permission classes to settings:

        REST_FRAMEWORK = {
            'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
        }

- Create a permissions.py file in both apps with following code that returns a boolean value for owner of th ecurrent object:

        class IsOwner(permissions.BasePermission):
            def has_object_permission(self, request, view, obj):
                return obj.owner == request.user 


#### 1. RegisterView:

- Create a view by extending CreateAPIView. The serializer_class tells which serializer to use and the permission_classes handles who can access the API.
- Allow any user (authenticated or not) to hit this endpoint.
- serializer = self.serializer_class(data=request.data) restore those native datatypes into a dictionary of validated data.
- serializer.is_valid(raise_exception=True) checks if the data is as per serializer fields otherwise throws an exception.
- serializer.save() to return an object instance, based on the validated data.

- Generate jwt token using user details :

        payload = jwt_payload_handler(user)
        token = jwt.encode(payload,settings.SECRET_KEY)   

- Create email verification link :  

        absurl = 'http://'+current_site+relativeLink+'?token='+str(token)

- Short this link by using pyshortners. 
- Send token on given email id:
    - Create a file in app named as Utils.py :  

            from django.core.mail import EmailMessage

    - Using EmailMessage() we can send this verification link on email.
    - Other variables need to be set to send email:
        In settings.py:

            EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            EMAIL_USE_TLS = True
            EMAIL_HOST = 'smtp.gmail.com'
            EMAIL_PORT = 587
            EMAIL_HOST_USER = 'abc@gmail.com'
            EMAIL_HOST_PASSWORD = '***'
     
#### 2. VerifyEmail view:
- Get token from url and decode it to fetch user details.
- Check token validations.If not then raise jwt errors.
- Set the is_active and is_verified field as true :  

        payload = jwt.decode(token,settings.SECRET_KEY)
        user = User.objects.get(id=payload['user_id'])
        if not user.is_verified:
            user.is_verified=True
            user.is_active=True
            user.save()
    
#### 3. LoginView:
- Create a post method.
- Set serializer class and pass request data to it for validations.
- Check if user exists or not, if not then raise error.  

        def validate(self, attrs):
            email= attrs.get('email','')
            password = attrs.get('password','')
            try:
                user = User.objects.get(email =email, password=password)
                if not user:
                    raise AuthenticationFailed("Invalid credentials given!!!")
                if not user.is_active:
                    raise AuthenticationFailed("Account is deactivated!!!")
                if not user.is_verified:
                    raise AuthenticationFailed("Email is not verified!!!")
            except serializers.ValidationError as identifier:
                return {'error':"Please provide email and password"}
            return {
                'email':user.email,
                'username':user.username,
                'password':user.password,
            }

- Otherwise create jwt token for it and return details in response.

#### 4. ResetPassword View:

- Take email from user validates it to generate jwt token.
- Create link using token and send it to user email.
- If email does not exist then raise validation error.
- Use pyshortners to short this verification link.

#### 5. NewPassword View:

- Get token from url and decode it using jwt.decode().
- fetch user details from it.
- check if token is valid or not, if it is then set new validated password for user.
- Otherwise raise jwt exceptions.  
    
        try:
            payload = jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            user.password = user_data['password']
            user.save()    
            return Response({'email':'New password is created'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Link is Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

#### 5. Logout View:

- Set permsission as IsAuthenticated. So only authenticated and logged in user will be able to access it.
- Call logout() 

#### 6. UserProfile view:

- Use RetreiveUpdate from generics that will provide views to update user profile.
- to get current user profiel rewrite the get_object method :
    
        def get_object(self):
            return self.request.user.profile

### View for notes app:

- Every view is calss based and following attribues need to be set for each:

    * serializer_class : serilaizer class
    * queryset : Model object 
    * permission_classes = (permissions.IsAuthenticated, IsOwner)

#### 1. CraeteAndListNotes :
- It will extend CreateAndListView from generics of rest frame work.
- It provides following views :
    * Post : To create a new note.
    * Get : To list all created notes for a user.
- Pass request data to NotesSerializer for validation and serialized data with current user id.
- Re write perform_create method to save data and get_queryset() to get records from database.

#### 2. NoteDetails view:

- It extends RetrieveUpdateDestroyView from generics.
- It provides look-up field to get note by its id.
- It provides views :
    * get :  To retrieve note .
    * (put, patch) : To update note .
    * delete : To delete note.

#### 3. CreateAndListLabels view :

- It will extend CreateAndListView from generics of rest frame work.
- It provides following views :
    * Post : To create a new label.
    * Get : To list all created labels for a user.

#### 4. LabelDetails view:

- It extends RetrieveUpdateDestroyView from generics.
- It provides look-up field to get note by its id.
- It provides views :
    * get : To retrieve label.
    * (put, patch) : To update label.
    * delete : To delete label.

#### 5. ArchiveNote view:

- It extends RetrieveUpdateDestroyView from generics.
- It provides look-up field to get note by its id.
- It provides views :
    * (put, patch) : To update archive field's value of note.

#### 6. NoteToTrash view : 

- It extends RetrieveUpdateDestroyView from generics.
- It provides look-up field to get note by its id.
- It provides views :
    * (put, patch) : To update isDelete field's value of note.

#### 7. ArchiveNotesList view : 

- It extends ListAPIView from generics.
- It provides views :
    * get : To get all notes with archive field's value as true.

#### 8. TrashList view : 

- It extends ListAPIView from generics.
- It provides views :
    * get : To get all notes with isDelete field's value as true.

#### 9. AddLabelsToNote view : 

- It extends RetrieveUpdateDestroyView from generics.
- It provides look-up field to get note by its id.
- It provides views :
    * (put, patch) : To update add label list to note.
- To get list of all created labels, in serializer of this class give a queryset parameter as following:

        class AddNotesInLabelsSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):
            class Meta:
                model= Labels
                fields=['name']

        class AddLabelsToNoteSerializer(serializers.ModelSerializer):
            label =AddNotesInLabelsSerializer(many=True, queryset=Labels.objects.all())

#### 10. ListNotesInLabel view :

- Use same serializer class as AddLabelsToNote view.
- Rewite the get_queryset() to filter queryset according to label id given in lookup field:

        def get_queryset(self):
            return self.queryset.filter(owner=self.request.user,label=self.kwargs[self.lookup_field])            

- It provides views :
    * get : To get all notes list with smae label.

#### 11. SearchNote view : 
- Get the search parameter and pass it to the get_queryset() :  
        
            Request.GET.get('search')

- Override the get_queryset() to match the search parameter with records data.
- To match the search query parameter with model field data, use icontains lookup. It matches the data case insensetive :  

            fieldname__icontains

#### 12. AddCollaborator view :
- Create a field in notes model to add collaborator. 
- Give pemission to added user in colloborator field to access note .
- To give permissions overrid the permission methods.


### Create route 

- For every view we have to create route in urls.py in its correspnding app.
- To access these APIs the corrosponding path has to be provided on localhost.  

        urlpatterns = [
            path('register/',RegisterView.as_view() , name='register'),
            path('login/',LoginAPIView.as_view() , name='login'),
            path('logout/', LogoutView.as_view(), name='logout'),
            path('verify-email/',VerifyEmail.as_view() , name='verify-email'),
            path('reset-password/',ResetPassword.as_view() , name='reset-password'),
            path('new-pass/', NewPassword.as_view(), name='new-pass'),
            path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        ]

### Write Test Cases :
- Create test folder in both apps.
- In test folder create two files : 
    * test_models.py
    * test_views.py
- To create test class import extend TestCase : 

        from django.test import TestCase

- In test case file create a test client by craeting object of Client class : 

        self.client = Client()

- In setUp method create dumy records to perform test cases.
- In every test case call API give data to be post and check the response dtaa and code.
- Use assertEqual and assertNotEqual to match the output of test case with desired output.
- Try to write test cases for every possible condition while calling APIs.
- Create valid and invalid data in dictionary object to be post, so that both positive and negative outputs can also be tested.
- Example Test case for view :

        def test_get_all_notes_after_login(self):
            self.client.post(reverse('login'),data=json.dumps(self.user1_credentials), content_type='application/json')
            notes = Notes.objects.filter(owner=self.user1, isArchive=False, isDelete=False)
            serializer = NotesSerializer(notes, many=True)
            response = self.client.get(reverse('notes'))
            self.assertEqual(response.data, serializer.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

- Example test case for model test:

        def test_create_note(self):
            note = Notes.objects.get(title='first note')
            self.assertEqual(note.get_content(), "this is my first note")


### SonarQube Analysis:

#### Isntall sonarQube form zipfile:

* Download sonarQube community version from this link : https://www.sonarqube.org/downloads/
* Unzip it and configure properties and config files inside conf folder:
  - sonar.properties file :
    1. Setting the Access to the Database:Uncomment these lines and set variables
        Example for PostgreSQL
		- sonar.jdbc.username=sonarqube
		- sonar.jdbc.password=
		- sonar.embeddedDatabase.port=9092
		- sonar.jdbc.url=jdbc:postgresql://localhost/sonarqube?currentSchema=my_schema
	2. Starting the Web Server
		- sonar.web.host=127.0.0.1
		- sonar.web.context=
		- sonar.web.port=9000
		
   - wrapper.conf file:
     1. Adjusting the Java Installation
	 	- wrapper.java.command=/path/to/my/jdk/bin/java
		
* Execute the following script to start the server:
	- On Linux: bin/linux-x86-64/sonar.sh start
	- On macOS: bin/macosx-universal-64/sonar.sh start
	- On Windows: bin/windows-x86-64/StartSonar.bat
	We can now browse SonarQube at http://localhost:9000 (the default System administrator credentials are admin/admin).

* After the installation:
	- After server is up and running, we'll need to install one or more SonarScanners on the machine where analysis will be performed.
	- Use this link to download: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
	
### Running SonarScanner from the zip file

To run SonarScanner from the zip file, follow these steps:
* Expand the downloaded file into the directory of your choice. We'll refer to it as $install_directory in the next steps.
* Update the global settings to point to your SonarQube server by editing $install_directory/conf/sonar-scanner.properties:
	- #sonar.host.url=http://localhost:9000
* Add the $install_directory/bin directory to your path.
* Verify installation by opening a new shell and executing the command sonar-scanner -h (sonar-scanner.bat -h on Windows). Output soulbe be like this:    


            usage: sonar-scanner [options]
            Options:
            -D,--define <arg>     Define property
            -h,--help             Display help information
            -v,--version          Display version information
            -X,--debug            Produce execution debug output

	
### Configuring your project:

* Create a configuration file in your project's root directory called sonar-project.properties:  

            - sonar.projectKey=my:project
            - #sonar.projectName=My project
            - #sonar.projectVersion=1.0
            - #sonar.sources=.
            - #sonar.sourceEncoding=UTF-8

### Launching the project:

* Give a project on the server 
* Generate a token
* Run the following command from the project base directory to launch analysis and pass your authentication token:
	    
        sonar-scanner -Dsonar.login=myAuthenticationToken

### Now browse SonarQube at http://localhost:9000 :

![Alt text](https://github.com/bHartiii/Keep-Notes/blob/Development/media/screenshots_readme/screenshot-sonarqube.png?raw=true)


### Redis Installation : 

* **About redis** : Redis is an in-memory data structure store that can be used as a caching engine. Since it keeps data in RAM, Redis can deliver it very  quickly. Redis is not the only product that we can use for caching.
* Use this link to download redis for windows: https://github.com/MicrosoftArchive/redis/releases
* Download and run .msi file for installation. 

![Alt text](https://github.com/bHartiii/Keep-Notes/blob/Development/media/screenshots_readme/redis-git-repo.png?raw=true)

* Check the add path to enviornment while installation or add redis in enviornment variable manually:

![Alt text](https://github.com/bHartiii/Keep-Notes/blob/Development/media/screenshots_readme/redis-add-path.png?raw=true)

* Open command prompt and give following command to start redis server:
    - redis-cli
    - Type ping to check if server is started or not. it should return pong as response.

    - ![Alt text](https://github.com/bHartiii/Keep-Notes/blob/Development/media/screenshots_readme/Command-Prompt-redis-cli.png?raw=true)


### Redis cache implementation :

- Set custom cache backend in settings :  

        CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache", 
                "LOCATION": "redis://127.0.0.1:6379/1",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                    "TIMEOUT": 3600
                },
                "KEY_PREFIX": "keep"
            }
        }

- **Accessing the cache**:
    - import : from django.core.cache import cache
    - cache.set(key, value, timeout=DEFAULT_TIMEOUT, version=None)
    - cache.get(key, default=None, version=None)
    
- For each API call check if data is present in cache or not by using cache.get(key).
- If it is there then retrieve data from to cache only otherwise perform query on database and set that data to cache by using cache.set(key, data).
So that next time that data can be retrieved from cache.


### RabbitMQ Installation:
- First we need to download and install erlang from the given link for windows: https://erlang.org/download/otp_versions_tree.html

 - ![Alt text](https://github.com/bHartiii/Keep-Notes/blob/Development/media/screenshots_readme/install-erlang.png?raw=true)

- Then we need to download and install rabbitMQ server for windows : https://www.rabbitmq.com/install-windows.html

 - ![Alt text](https://github.com/bHartiii/Keep-Notes/blob/Development/media/screenshots_readme/rabbitMQ-server-install.png?raw=true)

- then go to start menu and search for rabbitmq command prompt
- type command "rabbitmq-plugins enable rabbitmq_management"
- All set to go now go to http://localhost:15672
- Use following credentials for authentication:
    - username: guest
    - passowrd: guest 

### Celery Basic Setup:

- Add the CELERY_BROKER_URL configuration to the settings.py file :  
            
            CELERY_BROKER_URL = 'amqp://localhost'

- In project root folder create a new file named celery.py and add the following code in that :

            import os
            from celery import Celery

            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

            app = Celery('project_name')
            app.config_from_object('django.conf:settings', namespace='CELERY')
            app.autodiscover_tasks()

- Now edit the __init__.py file in the project root:

            from .celery import app as celery_app
            __all__ = ['celery_app']

- Create a file named tasks.py inside a Django app and put all our Celery tasks into this file. Basic structure is here :  

            from celery import shared_task

            @shared_task
            def name_of_your_function(optional_param):
                pass  # do something heavy

- **Starting The Worker Process :**
    Open a new terminal tab, and run the following command:

            celery -A mysite worker -l info

### Asychronous tasks in celery:

- To check the task status install django_celery_results package. It store the status of tasks in databse table.
- We have to add this in installed apps settings and then migrate.
- Add Celery backend as django database in settings :

            CELERY_RESULT_BACKEND = 'django-db'

- Add celery cache as django cache also in settings:

            CELERY_CACHE_BACKEND = 'django-cache'

### Setting periodic tasks in celery:
- Install celery_beat extension for this and add it to installed apps in settings.
- After this migrate all migrations.
- Then celery.py file add the configuration for schedule beat like tasks name, scheduling time, and arguments for the method:
           
            app.conf.beat_schedule = {
                'triggering' : {
                    'task': 'Notes.tasks.send_email',
                    'schedule': 15,
                    'args': ('malibharti5@gmail.com',)
                }
            }

- To set schedule time we can use contrab and sonar schedulers also like this:

            contrab(minutes='*/15')

### Executing celery task:
- Run command : 

            celery -A KeepNotes beat -l info

### Monitoring Celery tasks:
- **celery -A KeepNotes status** : To check the status of every runnning worker.
- **celery -A KeepNotes inspect** : It take an agrguments like the following -
    1. active : Shows all running tasks in worker.
    2. reserved : Displays reserved tasks means those tasks that are not started and scheduled over max limit of worker. So these tasks will be executed whenever the worker will be free.
    3. schedule : Shows the periodic tasks.To set periodic tasks we have to set ETA or countdown parameters whilw calling asynchronous tasks.



### References :
- For redis cache implementation : https://docs.djangoproject.com/en/3.1/topics/cache/
- For rabbitMQ installation :
    - ubuntu : https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html
    - windows : https://www.youtube.com/watch?v=V9DWKbalbWQ
- For celery : 
    1. https://simpleisbetterthancomplex.com/tutorial/2017/08/20/how-to-use-celery-with-django.html
    2. https://www.youtube.com/watch?v=A89mCa1ytow
