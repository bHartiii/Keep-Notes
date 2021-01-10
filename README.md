# Keep-Notes

**Description** : 
- This is django Project in which rest APIs are created for authentication.  
- It provides APIs for following features:
    * Registration using email verification.
    * Login and logout
    * Reset password
    * UserProfile 
- For authentication JWT token is used. 
- For user profile creation signal is used.
- **JWT Token :** JWT is an encoded JSON string that is passed in headers to authenticate requests. It is usually obtained by hashing JSON data with a secret key. This means that the server doesn't need to query the database every time to retrieve the user associated with a given token.  

- **The Concept of Authentication and Authorization:**  
Authentication is the process of identifying a logged-in user, while authorization is the process of identifying if a certain user has the right to access a web resource.

- **Signals** : Django includes a “signal dispatcher” which helps allow decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place. They’re especially useful when many pieces of code may be interested in the same events.

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


### Create Models For App:

- In Django models are used to define the database layout or in simple terms tables in the database.
- There are two models:
    1. User
    2. UserProfile
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

- Create a image field in user profile model. 
- There is one to one relation between user and profile.

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
        ]


- Register models in admins.py:

        from django.contrib import admin
        from authentication.models import User, UserProfile
        admin.site.register(User)
        admin.site.register(UserProfile)


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
            python manage.py migrate
            Operations to perform:   #output
            Apply all migrations: admin, auth, contenttypes, userprofile, sessions, user
            Running migrations:
                Applying user.0001_initial... OK
                Applying userprofile.0001_initial... OK


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

- Create serializers.py file inside the app and create following serializer for every view in the views.py:
    1. RegisterSerializer
    2. EmailVerificationSerializer
    3. LoginSerilaizer
    4. ResetPasswordSerializer
    5. NewPasswordSerializer
    6. UserProfilrSerializer

- Create class that extends the serializer.
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



### Create views:

- Create the endpoint for registering the user by creating views.py file under user.
- All views are class based and inherit generic views.
- In every view class permission and serialzer_class has to be set.
- For permissions add these permission classes to settings:

        REST_FRAMEWORK = {
            'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
                'rest_framework.authentication.SessionAuthentication',
                'rest_framework.authentication.TokenAuthentication',
                'rest_framework.authentication.BasicAuthentication',
            ),
        }


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

### Create route 

- For every view we have to create route in urls.py in app.
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