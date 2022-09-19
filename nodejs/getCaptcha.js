const { chromium } = require('playwright');
const { FingerprintGenerator } = require('fingerprint-generator');
const { FingerprintInjector } = require('fingerprint-injector');

(async () => {
    let proxy = process.argv[2]
    let username = process.argv[3]
    let password = process.argv[4]
//     const b = await chromium.launch({
//   proxy: {
//     server: proxy,
//     username: username,
//     password: password
//   }
// , headless: false});
    const b = await chromium.launch({headless: false})
    const ctx = await b.newContext();

    const fingerprintGenerator = new FingerprintGenerator();
    const fingerprintInjector = new FingerprintInjector();

    const fingerprint = fingerprintGenerator.getFingerprint({
        'locales': ['ru-RU'],
        'operatingSystems': ['windows'],
    });
    //await fingerprintInjector.attachFingerprintToPlaywright(ctx, fingerprint);
    const page = await ctx.newPage();
    await page.goto("https://www.warframe.com/resetpassword");
    await page.locator('#confirm-email > input').fill('gfihsfseife@gmail.com');

    // let token = await page.evaluate(`grecaptcha.enterprise.execute("6LcWYwYgAAAAAIw9zG71CAPMr2oJPm3zpiaCXLVj", {action: "forgotpw"}).then(function(token) {
    //                         return token
    //                     });`)
    // console.log(token)
    // await ctx.close()
    // process.exit()
})();