import undetected_chromedriver as uc
import multiprocessing
import time


def solve_captcha():
    start = time.time()
    multiprocessing.freeze_support()
    chrome_option = uc.ChromeOptions()
    chrome_option.add_argument("--headless")
    driver = uc.Chrome(options=chrome_option)
    try:
        driver.get('https://www.warframe.com/resetpassword')
        while True:
            if driver.execute_script('return document.readyState;') == "complete":
                break
        result = driver.execute_script('''async function getToken() {
    token = await grecaptcha.enterprise.execute("6LcWYwYgAAAAAIw9zG71CAPMr2oJPm3zpiaCXLVj", {action: "forgotpw"}).then(function(token) {
                                return token
                            });
    return token}
    token = await getToken()
    return token''')
        print(time.time() - start)
        driver.close()
        return result
    except:
        driver.close()
        return None