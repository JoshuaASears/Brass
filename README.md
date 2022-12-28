<head>
    <h1>Brass</h1>
    <p>A minimalist application for creating and storing passwords. Use on trusted devices only!</p>
</head>
<body>
    <h3>v0.11 Release Notes -- 12/28/2022</h3>
    <p>v0.11 is a minimum viable product. It is password manager for Windows desktop designed to generate customizable random password strings and save them to a Domain/Username.</p>
    <h3>Setup</h3>
    <p>The following directory and files is required for use. Folders are in <b>bold</b>, files in <i>italics</i>.</p>
    <ul>
        <li><b>Brass</b></li>
        <ul>
            <li><b>Data</b></li>
                <ul>
                    <li><i>keyring.db</i></li>
                    <li><i>exported_keyring.txt</i></li>
                </ul>
            <li><i>Brass.ico</i></li>
            <li><i>Brass.exe</i></li>
        </ul>
    </ul>
    <h3>Use Instructions</h3>
    <ol>
        <li>Click on <i>Brass.exe</i> to begin.</li>
        <li>The first frame of the program is the Profile Frame. In the field, enter desired Username. To access data after program is shutdown, this same Username will need to be entered. There is no limit to how many profiles may exist, but you may not have more than 1 profile with the same name, as there is no way for the program to differentiate them.</li>
        <li>The next frame is the Manager Frame. The Manager Frame allows you to add a Domain, Username, and Password (Key) to the database. Domains (ex: Google, Reddit) and Usernames are not saved to the database independently. Instead, you save a Domain with its Username with its Key. You may save multiple Usernames/Keys to a Domain, but they are always saved as a set. You may manually enter a Key or use the 'Generator New' button to generate a random Key with the character requirements set on the right. After you are satisfied with your Domain/Username/Key, then hit 'Save Key.' This saves the Domain/Username/Key set. <u>The Generate New button does not save your information</u>.</li>
        <li>After your initial save, you may use the dropdown selectors to access the Domains and Usernames you have stored in the database. Or you may continue to manually enter in new Domain/Usernames.</li>
        <li>Access your most recent saved Keys by selecting your Domain/Username. This will populate your most current Key in the Key field. If you want to update your Key for a Domain/Username, simply type over your old one or use the Generator and then hit save. You will be able to see your new Key again by selecting the Domain/Username.</li>
        <li>You may export a printable list of the most current Keys for all your Domain/Username by using the 'Export .txt' button. This outputs to the <b>data</b> folder in the program directory. The other file in the <b>data</b> folder is the database used for your profile.</li>
    </ol>
    <h3>Build</h3>
    <p>Brass is built using the following python 3.11 builtin modules: tkinter, sqlite, string, date, random, and time. The source code are main.py (root window, main loop), interface.py (GUI and flow control) and keyring.py (data persistence). The exe has been compiled using pyinstaller. Scripting by Joshua Sears.</p>
</body>