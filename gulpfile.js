var gulp = require('gulp');
var del = require('del');
var mainGulpBowerFiles = require('main-bower-files');
var $ = require('gulp-load-plugins')();
var pkg = require('./package.json');

var app = {
    src: 'frontend/app/',
    tsDef: 'typings/',
    assets: 'frontend/assets/',
    output: 'public/',
};

var buildArtifact = {
    assets: 'assets/',
    vendorCss: 'vendor.css',
    vendorJs: 'vendor.js',
    appJs: 'app.js',
    appCss: 'app.css',
    appTemplate: pkg.name + '.tpl.js'
};

var templateOptions = {
    module: 'app'
};

var minifyHtmlOptions = {
    empty: true,
    loose: true
};

/**
 * Build all third party libraries
 */
gulp.task('build-vendor', function () {
    var jsFilter = $.filter('**/*.js', { restore: true });
    var cssFilter = $.filter(['**/*.css'], { restore: true });
    var fontFlter = $.filter('**/*.{ttf,woff,woff2,eof,svg}');
    return gulp.src(mainGulpBowerFiles())
        // js
        .pipe(jsFilter)
        .pipe($.concat(buildArtifact.vendorJs))
        .pipe(gulp.dest(app.output + buildArtifact.assets))
        .pipe(jsFilter.restore)

        // css
        .pipe(cssFilter)
        .pipe($.concat(buildArtifact.vendorCss))
        .pipe($.replace("url('..", "url('../assets/"))
        .pipe(gulp.dest(app.output + buildArtifact.assets))
        .pipe(cssFilter.restore)

        // font
        .pipe(fontFlter)
        .pipe($.rename({ dirname: '' }))
        .pipe(gulp.dest(app.output + buildArtifact.assets +'fonts/'));
});

/**
 * Remove all files under the 'www' folder
 */
gulp.task('clean', function () {
    del.sync(app.output);
});

/**
 * Generate index html page to the public
 */
gulp.task('generate-index-html', function () {
    return gulp.src('frontend/index.html')
        .pipe($.template(buildArtifact))
        .pipe(gulp.dest(app.output));
});

/**
 * Copy over the assets folder
 */
gulp.task('copy-assets', function () {
    gulp.src(app.assets + '**/*.*')
        .pipe(gulp.dest('public/assets'));
});

/**
 * Build for JS
 */
gulp.task('compile-typescript', function () {
    var tsCompiler = gulp.src([app.src + '**/*.ts', app.tsDef + '**/*.ts'])
        .pipe($.sourcemaps.init())
        .pipe($.typescript({
            typescript: require('typescript'),
            noImplicitAny: false,
            removeComments: true,
            noEmitHelpers:true,
            noExternalResolve: true,
            out: buildArtifact.appJs
        }));

    return tsCompiler.js
        .pipe($.replace(/'use strict';/g, ''))
        .pipe($.replace(/\/\/\/ <reference path="(.*)" \/>/g, ''))
        .pipe($.uglify())
        .pipe($.sourcemaps.write())
        .pipe(gulp.dest(app.output + buildArtifact.assets));
});

/**
 * Generate html template cache for partials
 */
gulp.task('build-partial-cache', function () {
    return gulp.src(app.src + '**/*.html')
         .pipe($.minifyHtml(minifyHtmlOptions))
         .pipe($.angularTemplatecache(buildArtifact.appTemplate, templateOptions))
         .pipe(gulp.dest(app.output + buildArtifact.assets));
});

/**
 * Default gulp task
 */
gulp.task('default', function () {
    console.log('No default task defined yet');
});

gulp.task('build', [
    'clean',
    'build-vendor',
    'copy-assets',
    'compile-typescript',
    'build-partial-cache',
    'generate-index-html'
]);