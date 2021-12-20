# Lab 8: Email Confirmation

>The main goal of this lab work is to create an application that could register a new user. However, the
application must also require email confirmation (via a one time password / code or via a link).
After confirming their email, a user should be able to see that their email is confirmed.

### Required features:

- Create an application that could register a new user;
- Perform email confirmation (via a one time password / code or via a link);
- Output on the screen whether a user confirmed their email or did not confirm it yet.


### Used Technologies:

- Windows 10 
- Java
- IntelliJ IDEA
- Java Swing
- Java Mail


### Instructions:

**1. Create a file named login.properties with the following structure:**
*(it will keep the user and password for the sender's gmail):*

```
user=your_username
password=your_password
```

**2. Write the path to this file in the following row:**
```
58. FileReader reader=new FileReader("properties_path_here");
```

**3. Run GUI.java**
