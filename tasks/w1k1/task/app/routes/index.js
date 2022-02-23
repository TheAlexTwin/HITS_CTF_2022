var express = require('express');
var router = express.Router();
const { exec } = require("child_process");


/* GET home page. */
router.get('/', function (req, res, next) {
    let s = req.query.search;

    if (s) {
        exec("wikit " + s, (error, stdout, stderr) => {
            if (error) {
                return res.status(400).send({
                    message: error.toString()
                });
            }
            if (stderr) {
                return res.status(400).send({
                    message: error.toString()
                });
            }
            res.render('index', {title: "Suitable article", text: stdout});
        });
    } else {
        res.render('index');
    }
});

module.exports = router;
