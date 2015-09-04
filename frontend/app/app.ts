/// <reference path="../../typings/tsd.d.ts" />

(():void => {
    'use strict';
    angular.module('app', ['ui.router']);

    // Route configuration
    function routeConfig(
        $stateProvider: ng.ui.IStateProvider,
        $urlRouterProvider: ng.ui.IUrlRouterProvider
    ) {
        $stateProvider.state('home', {
            url: '/',
            templateUrl: 'partials/home.tpl.html',
            controller: 'homeController'
        });
        $urlRouterProvider.otherwise('/');
    }
    routeConfig.$inject = ['$stateProvider', '$urlRouterProvider'];

    angular.module('app').config(routeConfig);
})();