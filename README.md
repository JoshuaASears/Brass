<head>
    <h1>Brass</h1>
    <p>A minimalist application for creating and storing passwords. Use on trusted devices only!</p>
</head>
<body>
    <h3>v0.11 Release Notes -- 12/28/2022</h3>
    <p>This release is a minimum viable product. It is password manager for Windows desktop designed to generate customizable random password strings and save them to a Domain/Username.</p>
    <h3>Setup</h3>
    <p>For use of the application, download the Brass v0.11.zip. Extract folder and all contents to C:\Users\[user]\AppData\Local or other folder*. Wherever you store the program folder on your device, ensure that all sub files and folders maintain the following organization (folders are in <b>bold</b>, files in <i>italics</i>):</p>
    <ul>
        <li><b>Brass v0.11</b></li>
        <ul>
            <li><b>data</b></li>
                <ul>
                    <li><i>keyring.db</i></li>
                    <li><i>exported_keyring.txt</i></li>
                </ul>
            <li><i>Brass.ico</i></li>
            <li><i>Brass.exe</i></li>
            <li><i>README.md</i></li>
        </ul>
    </ul>
    <p>*Known Issue: application will not work if extracted to the Program Files directory. An artifact of this issue is if the "Enter Profile" button exists above the "Domain" label of the following program frame. If this happens, then the directory that the program folder has been extracted to will not work. Choose a new directory (such as the suggested directory above), or try running as administrator to resolve.</p>
    <h3>Use Instructions</h3>
    <ol>
        <li>Click on <i>Brass.exe</i> to begin.</li>
        <li>In the first frame of the program, enter your desired profile. Once a profile is entered, the program will open the Manager Frame. All data saved in the Manager frame is associated with your profile. There is no limit to how many profiles may exist, but you may not have more than 1 profile with the same name, as there is no way for the program to differentiate them.</li>
        <li>The Manager Frame allows you to add a Domain, Username, and Password (Key) to the database. Domains (ex: Google, Reddit, etc.) and Usernames are not saved to the database independently. Instead, the program requires a set of strings to save together: Domain + Username + Key. You may save multiple Usernames/Keys to a Domain, but they are always saved as a set. You may manually enter a Key or use the 'Generate New' button to generate a random Key with the character requirements which can be toggled in the lower right of the GUI. After you are satisfied with your Domain/Username/Key, then hit 'Save Key.' This saves the Domain/Username/Key set to the database. <u>The Generate New button does not save your information</u>.</li>
        <li>After your initial save, you may use the dropdown selectors to access the Domains + Usernames you have stored in the database. Or you may continue to manually enter in new Domain/Usernames.</li>
        <li>Access your most recent saved Keys by selecting your Domain/Username. This will populate your most current Key in the Key field. If you want to update your Key for a Domain/Username, simply type over your old one or use the Generator and then hit save. You will be able to see your new Key again by selecting the Domain/Username.</li>
        <li>You may export a printable list of the most current Keys for all your Domain/Username by using the 'Export .txt' button. This outputs the <i>exported_keyring.txt</i> file in the <b>data</b> folder of the program directory.</li>
    </ol>
    <h3>Build</h3>
    <p>Brass is built using the following Python 3.11 built-in modules: <i>tkinter</i>, <i>sqlite</i>, <i>string</i>, <i>date</i>, <i>random</i>, and <i>time</i>. The project specific source code is in <i>main.py</i> (root window with main loop), <i>interface.py</i> (GUI and flow control) and <i>keyring.py</i> (data persistence). <i>interface.py</i> and <i>keyring.py</i> source code is located in the <b>scripts</b> folder. The .exe has been compiled using <i>pyinstaller</i>. Scripting by Joshua Sears, 2022.</p>
</body>
