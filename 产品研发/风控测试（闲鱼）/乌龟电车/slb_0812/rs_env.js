delete __dirname
delete __filename


const fs = require('fs');
const proxyCache = {};  // 缓存已代理对象，避免重复代理
const isTable = false; // 是否表格输出

// Node属性、过滤属性、代理对象
const nodeProps = Object.getOwnPropertyNames(global)
const filters = nodeProps.concat(['proxyCache', 'nodeProps', 'uniques', 'filters', 'targets'])
const uniques = ["global", "process", "Buffer", "setImmediate", "clearImmediate"]
const targets = ["window", "document", "navigator", "location", "history", "screen", "localStorage", "sessionStorage"];

// 获取属性元素名称
function toDomProp(value, target, prop) {
    const tag = prop[0].toUpperCase() + prop.slice(1);
    const isElementCreation = target.includes('.createElement') || target.includes('.getElementsByTagName');

    if (isElementCreation) {
        // 如果 value 是数组，返回 '[object HTMLCollection]'
        if (Array.isArray(value)) {
            return 'HTMLCollection';
        }

        return prop.length > 1
            ? `HTML${tag}Element`
            : {
                p: 'HTMLParagraphElement',
                q: 'HTMLQuoteElement',
                a: 'HTMLElement',
                b: 'HTMLElement',
                i: 'HTMLElement',
                s: 'HTMLElement',
                u: 'HTMLElement'
            }[prop]
            || 'HTMLUnknownElement';
    }

    const special = {document: 'HTMLDocument', sessionStorage: 'Storage', localStorage: 'Storage'};
    if (prop in special) return special[prop];
    if (value === global) return 'Window';
    if (prop === 'prototype') return target;
    return targets?.includes(prop) ? tag : 'Object';
}

// 格式化输出
function formatValue(value, target, prop) {
    const type = typeof value;
    if (type === 'string') {
        const max_length = 70;  // 默认显示 70 个字符
        return value.length > max_length ? `${value.substring(0, max_length)}...` : value;
    } else if (type === 'object') {
        prop = typeof prop === 'string' ? toDomProp(value, target, prop) : 'Object'
        if (isTable) {
            return value === null ? null : `[object ${prop}]`;
        }else{
            return value === null ? null : `\x1b[36m[object ${prop}]\x1b[0m`;  // 颜色输出
        }
    }
    return value;
}

// 自动代理对象
function autoProxy(target, namePath) {
    const split = String(namePath).split('.')
    const prop = split.pop(), source = split.shift()

    // 如果结果类型不是对象（非数组）或函数，或为 window 对象，则不进行代理
    if (!(typeof target === 'object' && target !== null && !('length' in target)) && typeof target !== 'function' || 'global' in target) return target;

    // 如果属性不是字符串类型、或第一个字符不是字母、或为过滤属性，则不进行代理
    if (typeof prop !== 'string' || !prop.match(/^[a-zA-Z]/g) || filters.includes(prop)) return target

    // 检查缓存是否存在，返回对象或者函数的代理
    if (source === 'window') namePath = namePath.replace("window.", "")
    if (namePath in proxyCache) return proxyCache[namePath];

    // 创建代理
    console.log(`\x1b[91m[代理] ${namePath}\x1b[0m`)
    const proxy = createProxy(target, namePath)
    proxyCache[namePath] = proxy  // 存入缓存
    return proxy
}

// 创建代理
function createProxy(target, namePath) {
    return new Proxy(target, {
        get(obj, prop) {
            // 获取属性名称
            const fullPath = `${namePath}.${String(prop)}`;

            // 如果属性为 Node 属性，则返回 undefined
            if (uniques.includes(prop)) {
                // 表格输出
                if (isTable) {
                    console.table({
                        "Get": {
                            '对象': namePath,
                            '获取属性': fullPath,
                            '返回值': '[Empty]',
                            '值类型': 'undefined'
                        }
                    });
                } else {
                    console.log(`\x1b[94m获取 ${fullPath}\x1b[0m -> \x1b[35m[empty]\x1b[0m`);
                }

                return undefined;
            }

            let value = Reflect.get(obj, prop);  // 获取属性值
            let result = autoProxy(value, fullPath);  // 自动代理

            // 如果属性不为过滤属性，则输出详细日志：属性名、值、类型
            if (!filters.includes(prop)) {
                // 表格输出
                if (isTable) {
                    console.table({
                        "Get": {
                            '对象': namePath,
                            '获取属性': `${fullPath}`,
                            '返回值': (n = formatValue(result, namePath, prop), typeof result === 'string' && result.length > 40) ? n.slice(0, 40) + '...' : n,
                            '返回值类型': typeof result
                        }
                    });
                } else {
                    console.log(`\x1b[94m获取 ${fullPath}\x1b[0m ->`, formatValue(value, namePath, prop))
                }
            }
            return result;
        },

        set(obj, prop, value) {
            // 获取属性名称
            const fullPath = `${namePath}.${String(prop)}`;

            // 解决 XMLHttpRequest 对象无法获取 open 方法的问题
            if (prop === 'XMLHttpRequest') {
                value.prototype = obj[prop].prototype
            }

            // 输出详细日志：属性名、设置的值、类型
            if (isTable) {
                console.table({
                    "Set": {
                        '对象': namePath,
                        '设置属性': `${fullPath}`,
                        '设置值': (n = formatValue(value, namePath, prop), typeof value === 'string' && value.length > 40) ? n.slice(0, 40) + '...' : n,
                        '设置值类型': typeof value
                    }
                });
            } else {
                console.log(`\x1b[91m设置 ${fullPath}\x1b[0m ->`, formatValue(value, namePath, prop))
            }

            return Reflect.set(obj, prop, value);
        },

        apply(func, thisArg, args) {
            // 执行函数并获取结果
            let value = Reflect.apply(func, thisArg, args);
            // 自动代理返回值
            if (args.length === 1 && typeof args[0] === 'string') {
                // 如果结果是数组，则代理数组第一个参数
                if (Array.isArray(value)) {
                    global[args[0]] = autoProxy(value[0], args[0])
                    value = Reflect.apply(func, thisArg, args)  // 重新执行函数
                } else {
                    value = autoProxy(value, args[0]);
                }
            }

            // 输出详细日志：函数名、参数、返回值、类型
            if (isTable) {
                let data = {
                    'Apply': {
                        '调用方法/参数值': namePath,
                    },
                }
                args.forEach((item, index) => {
                    data[`arg ${index + 1}`] = {
                        "调用方法/参数值": (n = formatValue(item, namePath, item), typeof item === 'string' && item.length > 40) ? n.slice(0, 40) + '...' : item,
                        "参数值类型": typeof item
                    }
                })
                data['return'] = {
                    '返回值': (n = formatValue(value, namePath, args[0]), typeof value === 'string' && value.length > 40) ? n.slice(0, 40) + '...' : n,
                    "返回值类型": typeof value
                }
                console.table(data)
            } else {
                console.log(`\x1b[92m调用 ${namePath}\x1b[0m`, args, '->', formatValue(value, namePath, args[0]))
            }

            return value;
        }
    });
}

// 初始化全局代理
function initGlobalEnv(targets) {
    // 初始化全局代理对象
    targets.forEach(t => {
        // 如果全局对象中不存在该属性，则创建一个空对象
        if (!global[t]) global[t] = {};

        // 创建代理对象并缓存
        global[t] = createProxy(global[t], t);
        proxyCache[t] = global[t]
    });
}

// 环境代码
window = global;

localStorage = {
    getItem: function (key) {
        return this[key]
    },
    setItem: function (key, val) {
        this[key] = val
    },
    removeItem: function (key) {
        delete this[key]
    }
}
sessionStorage = { ...localStorage }

window.top = window
window.addEventListener = function () {
}
location = {"ancestorOrigins": {}, "href": "https://ticket.sxhm.com/quickticket/index.html#/pages/sale/index", "origin": "https://ticket.sxhm.com", "protocol": "https:", "host": "ticket.sxhm.com", "hostname": "ticket.sxhm.com", "port": "", "pathname": "/quickticket/index.html", "search": "", "hash": "#/pages/sale/index"}

navigator = {
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090c0f) XWEB/11275 Flue",
    webdriver: false
};

div = {
    getElementsByTagName: function (arg) {
        if (arg === 'i') {
            return [];
        }
    }
};

script = {
    innerText: "",
    getAttribute: function (arg) {
        if (arg === 'r') {
            return 'm';
        }
    },
    parentElement: {
        removeChild: function (arg) {}
    }
};

meta = {
    content: content,
    parentNode: {
        removeChild: function (arg) {}
    },
    getAttribute: function (arg) {
        if (arg === 'r') {
            return 'm';
        }
    }
};

base = {
    getAttribute: function (arg) {
        if (arg === "href") {
            return null;
        }
    }
};

document = {
    documentElement: {},
    visibilityState: "visible",
    createElement: function (arg) {
        if (arg === 'div') {
            return div;
        } else if (arg === 'a') {
            return location;
        } else if (arg === 'form') {
            return {};
        }
    },
    appendChild: function (arg) {},
    removeChild: function () {},
    getElementById: function (arg) {},
    getElementsByTagName: function (arg) {
        if (arg === 'script') {
            return [script, script];
        }
        if (arg === 'meta') {
            return [meta, meta];
        } else if (arg === 'base') {
            return [base];
        }
    },
    addEventListener: function (arg) {}
};


window.CanvasRenderingContext2D = function () {
}

window.HTMLCanvasElement = function () {
}
window.HTMLFormElement = function () {}

window.HTMLAnchorElement = function () {
}

setTimeout = function () {
}
setInterval = function () {
}

window.XMLHttpRequest = function () {
}
window.XMLHttpRequest.prototype = {
    open: function (method, url) {
        return url
    },
    send: function () {
    }
}

function get_cookie() {
    return document.cookie
}

// 获取接口后缀
const URL = require('url');

function get_url(method, url) {
    // 生成url后缀，需要补环境： document.createElement('a') {return location};
    const parsedUrl = URL.parse(url);
    Object.keys(parsedUrl).forEach((key) => {
        if (parsedUrl[key] && key !== 'query') location[key] = parsedUrl[key];
    })
    return new XMLHttpRequest().open(method, url);
}

// 初始化代理对象
initGlobalEnv(targets);