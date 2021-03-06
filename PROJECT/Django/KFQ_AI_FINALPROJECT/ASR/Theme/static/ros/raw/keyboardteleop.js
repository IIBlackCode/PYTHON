var KEYBOARDTELEOP = KEYBOARDTELEOP || {
    REVISION: "0.3.0"
};
KEYBOARDTELEOP.Teleop = function (a) {
    var b = this;
    a = a || {};
    var c = a.ros,
        d = a.topic || "/cmd_vel",
        e = a.throttle || 1;
    this.scale = 1;
    var f = 0,
        g = 0,
        h = 0,
        i = new ROSLIB.Topic({ros: c, name: d, messageType: "geometry_msgs/Twist"}),
        j = function (a, c) {
            var d = f,
                j = g,
                k = h,
                l = !0,
                m = 0;
            switch (c === !0 && (m = e * b.scale), a) {
                case 65:
                    h = 1 * m;
                    break;
                case 87:
                    f = .5 * m;
                    break;
                case 68:
                    h = -1 * m;
                    break;
                case 83:
                    f = -.5 * m;
                    break;
                case 69:
                    g = -.5 * m;
                    break;
                case 81:
                    g = .5 * m;
                    break;
                default:
                    l = !1
            }
            if (l === !0) {
                var n = new ROSLIB.Message({
                    angular: {
                        x: 0,
                        y: 0,
                        z: h
                    },
                    linear: {
                        x: f,
                        y: g,
                        z: h
                    }
                });
                i.publish(n),
                (d !== f || j !== g || k !== h) && b.emit("change", n)
            }
        },
        k = document.getElementsByTagName("body")[0];
    k.addEventListener("keydown", function (a) {
        j(a.keyCode, !0)
    }, !1),
    k.addEventListener("keyup", function (a) {
        j(a.keyCode, !1)
    }, !1)
},
KEYBOARDTELEOP.Teleop.prototype.__proto__ = EventEmitter2.prototype;