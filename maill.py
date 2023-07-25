import smtplib

server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
server.login("example@gemail.com", "password")
server.sendmail("jmunene664@gmail.com",
                "jmunene664@gmail.com",
                "hello,how are you?")
server.quit()