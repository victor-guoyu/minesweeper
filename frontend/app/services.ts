/// <reference path="../../typings/tsd.d.ts" />
/// <reference path="./models.ts" />

module app.services {
    'use strict';
    import IResource = ng.resource.IResource;
    import IResourceService = ng.resource.IResourceService;

    class ApiService implements IApiService{
        static $inject = ['$log', '$resource'];
        constructor(
            private $log: ng.ILogService,
            private $resource: IResourceService
        ) {}

        api = <IGameResource> this.$resource('/game/:id', {id: '@id'},
            {
                createGame: {
                    url: '/game',
                    method: 'POST',
                    isArray: false
                },
                getGame: {
                    method: 'GET',
                    isArray: false
                },
                updateGame: {
                    method: 'POST',
                }
            });
    }

    angular.module('app').service('apiService', ApiService);
}