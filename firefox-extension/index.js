var self = require('sdk/self');

exports.dummy = dummy;

var pageMod = require("sdk/page-mod");

pageMod.PageMod({
  include: "*.facebook.com",
  contentScriptFile: [self.data.url("js/jquery-3.0.0.min.js"),
                      self.data.url("js/jquery-3.0.0.min.js"),
                      self.data.url("js/popup.js")],
  contentScriptOptions: {
    pngUrl: self.data.url("error.png")
  }
});
