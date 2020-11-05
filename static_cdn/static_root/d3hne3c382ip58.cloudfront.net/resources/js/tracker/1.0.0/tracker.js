const client = new ClientJS();
const access_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiOGUyMzBmZjNkOTg5NWI2MzQ3NGVkMTdkNmY2ZGY3NjQwMmJkMmQwZDlhZTk2ZDVlMDBkYTYwNDRiNjc3ZmQ3OWRhNDFmNjEwNTIxOGM2NzkiLCJpYXQiOjE2MDE4NzUyMjUsIm5iZiI6MTYwMTg3NTIyNSwiZXhwIjoxNjMzNDExMjI1LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.smtYRD0Isg12Ol5UABkDf3wOYXy3dOW9g5V8xn9kiPxMAAKtwp471CkS2O79-Hjd5-2yjGW4x3lL5JrESJdm8DptbjGJ0yWmhXcruzcTCt2rWojyfXKewSK2QK09ocl1-VhBhg2ycTe4Hi-xfU3c24VXcwxCOUywB8qtW1YfmggyC049Mod2Yec_mSa5SjLepYyGMbMEQ2wKgwij5W9aj22Zm8MRqtmIdF5lx2_-lWVF6QkI1bGrFVmw1QlUjLhqIo8wMAuRR8ZQba0pIS7CuVXN4uZ7Ti3yHhKp9pWxkcT7oU2Ar7IAg_zsiaLiwpmM23eqsDV8nqaDjOGHNSi5nMJCEhjQAz3kD1NJSnSdbUcWEkcNpBDXbuAH9QbqOP_PtnwUARiLqlNlLAbapuZNMXqtm8N5FpiTtB5FN1hNq6tvNbtGOvksTMxqvawltQqEa1nNf3ld7X-mSmAuRIlzGERnO3U31RbLRdDClUtx2_ZGQ7TJNMiNn892en0RtcQRRYfX37E44-VgoPEKYOhuMgCXhEK8cfSrSgVebPagUmAZ9J5BxbYIINW6V7pkjN3VDsmecTNAK0LibGNuh4yNYPCnC2QqwbsZjwTO7m19fy2aVKDDJLj5Yc2xp4ztjIQCKaI__zQM-UZPLUt0KfaQZT7cR9WRfmNtqFcUze88_g8';

var xhttp = new XMLHttpRequest();

class Tracker {

    browserMethods() {
        return {
            name: client.getBrowser(),
            version: client.getBrowserVersion(),
            engine: client.getEngine(),
            engine_version: client.getEngineVersion(),
        }
    }
    osMethods() {
        return {
            name: client.getOS(),
            version: client.getOSVersion()
        }
    }
    deviceMethods() {
        return {
            name: client.getDevice(),
            vendor: client.getDeviceVendor(),
            type: client.getDeviceType()
        }
    }

    getMobiletype() {
        if (client.isMobile()) {
            if (client.isMobileAndroid()) {
                return "android";
            } else if (client.isMobileIOS()) {
                return "ios";
            }
            else if (client.isMobileWindows()) {
                return "windows";
            }
            else if (client.isMobileOpera()) {
                return "opera";
            }
            else if (client.isMobileBlackBerry()) {
                return "blackberry";
            }
            return 'other'
        }
        return null;

    }
    mobileMethods() {
        return {
            is_mobile: client.isMobile(),
            type: this.getMobiletype()

        }
    }

    screenMethods() {
        return {
            resolution: client.getCurrentResolution(),
            color_depth: client.getColorDepth(),
            current_resolution: client.getAvailableResolution()

        }
    }

    getOtherInfo() {
        let infos = {};
        infos.installed_Plugin = client.getPlugins();
        if (client.isJava()) {
            infos.java = {};
            infos.java.installed = true;
            infos.java.getJavaVersion = client.getJavaVersion();
        }
        if (client.isMimeTypes()) {
            infos.mime_type = {};
            infos.mime_type.installed = true;
            infos.mime_type.available = client.getMimeTypes(); // Get Mime Types
        }

        return infos;

    }


    urlinfo() {
        return {
            current: window.location.pathname,
            base_uri: document.baseURI,
            referal: document.referrer
        }
    }

    track(serverdata) {
        let data = {
            fingerprint: "",
            userAgent: "",
            browser: {
                name: "",
                version: "",
                engine: "",
                engine_version: ""
            },
            os: {
                name: "",
                version: ""
            },
            device: {
                name: "",
                vendor: "",
                type: ""
            },
            cpu: "",
            mobile: {
                is_mobile: "",
                type: "",//ios,android
            },
            screen: {
                resolution: "",
                color_depth: "",
                current_resolution: ""
            },
            timezone: "",
            language: "",

            other: {
                installed_Plugin: "",
                java: {
                    installed: false,
                    version: null
                },
                mime_type: {
                    installed: false,
                    available: null
                }
            },
            activity: {
                page: "",
                referal: "",
            }


        };
        data.fingerprint = client.getFingerprint();
        data.userAgent = client.getUserAgent();
        data.browser = this.browserMethods();
        data.os = this.osMethods();
        data.device = this.deviceMethods();
        data.cpu = client.getCPU();
        data.mobile = this.mobileMethods();
        data.screen = this.screenMethods();
        data.timezone = client.getTimeZone();
        data.language = client.getLanguage();
        data.other = this.getOtherInfo();
        data.server = serverdata;

        data.activity = this.urlinfo();

        this.sendRequest({
            url: "https://tracker.bookmundi.com/post",
            method: "POST",
            payload: data
        })
    }

    sendRequest(data = {}) {
        var url = data.url;
        var params = JSON.stringify(data.payload);
        xhttp.open(data.method, url, true);

        //Send the proper header information along with the request
        xhttp.setRequestHeader('Content-type', 'application/json');
        xhttp.setRequestHeader('Authorization', access_token);

        xhttp.onreadystatechange = function () {//Call a function when the state changes.
            if (xhttp.readyState == 4 && xhttp.status == 200) {
             
            }
        }
        xhttp.send(params);
    }


    static start(data) {
        let t = new this;
        t.track(data);
    }

}

// module.exports = Tracker;
