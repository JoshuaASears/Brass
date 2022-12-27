<head>
    <h1>NakedKeyRing</h1>
    <p>A totally naked (not encrypted) KeyRing for creating and storing passwords. Must be used someplace safe or all your passwords become at risk!</p>
</head>
<body>
    <h3>v0.1 Release Notes -- 12/26/2022</h3>
    <p>v0.1 is a minimum viable product. It is a fully working password manager for Windows desktop designed to generate random password strings and save them to a Domain/Username.</p>
    <h3>Setup</h3>
    <p>The following assets and directory setup is required for use. Folders are in <b>bold</b>, files in <i>italics</i>.</p>
    <ul>
        <li><b>NakedKeyRing</b></li>
        <ul>
            <li><b>Data</b></li>
            <li><i>Keyring.ico</i></li>
            <li><i>NakedKeyRing.exe</i></li>
        </ul>
    </ul>
    <h3>Use Instructions</h3>
    <ol>
        <li>Click on <i>NakedKeyRing.exe</i> to begin.</li>
        <li>The first frame of the program is the Profile Frame. In the field, enter desired Username. To access data after program is shutdown, this same Username will need to be entered. There is no limit to how many profiles may exist, but you may not have more than 1 profile with the same name, as there is no way for the program to differentiate them.</li>
        <li>The next frame is the Manager Frame. The Manager Frame allows you to add a Domain, Username, and Password (Key) to the database. Domains (ex: Google, Reddit) and Usernames are not saved to the database independently. Instead, you save a Domain with its Username with its Key. You may save multiple Usernames/Keys to a Domain, but they are always saved as a set. You may manually enter a Key or use the 'Generator New' button to generate a random Key with the character requirements set on the right. After you are satisfied with your Domain/Username/Key, then hit 'Save Key.' This saves the Domain/Username/Key set. <u>The Generate New button does not save your information</u>.</li>
        <li>After your initial save, you may use the dropdown selectors to access the Domains and Usernames you have stored in the database. Or you may continue to manually enter in new Domain/Usernames.</li>
        <li>Access your most recent saved Keys by selecting your Domain/Username. This will populate your most current Key in the Key field. If you want to update your Key for a Domain/Username, simply type over your old one or use the Generator and then hit save. You will be able to see your new Key again by selecting the Domain/Username.</li>
        <li>You may export a printable list of the most current Keys for all your Domain/Username by using the 'Export .txt' button. This outputs to the <b>data</b> folder in the program directory. The other file in the <b>data</b> folder is the database used for your profile.</li>
    </ol>
    <h3>Build</h3>
    <p>NakedKeyRing is built using the following python 3.11 builtin modules: tkinter, sqlite, string, date, random, and time. The custom scripts are interface.py (GUI and flow control) and Keyring.py (data persistence). The exe has been compiled using pyinstaller.</p>
</body>