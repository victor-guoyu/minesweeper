/// <reference path="../../typings/tsd.d.ts" />

(():void => {
    'use strict';
    angular.module('app', ['ui.router', 'ngResource']);

    // Route configuration
    function routeConfig(
        $stateProvider: ng.ui.IStateProvider,
        $urlRouterProvider: ng.ui.IUrlRouterProvider
    ) {
        $stateProvider
            .state('home', {
            url: '/',
            templateUrl: 'partials/home.tpl.html',
            controller: 'homeController'
            })
            .state('play', {
                url: "/play/:game_id",
                templateUrl: 'partials/play.tpl.html',
                controller: 'playController',
                resolve: {
                    game: [
                        'gameModelBuilder',
                        '$stateParams',
                        (builder, $stateParams) => builder.getModel($stateParams.game_id)
                    ]
                }
            });
        $urlRouterProvider.otherwise('/');
    }
    routeConfig.$inject = ['$stateProvider', '$urlRouterProvider'];

    angular.module('app').config(routeConfig);
})();