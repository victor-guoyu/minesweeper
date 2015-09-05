/// <reference path="../../typings/tsd.d.ts" />
/// <reference path="./models.ts" />

module app.controllers {
    'use strict';
    class GameModelBuilder implements IModelBuilder<IGameModel> {

        static $inject = ['$log', 'apiService'];
        constructor(
            private $log: ng.ILogService,
            private apiService: IApiService
        ) {}

        getModel = (id: string):ng.IPromise<IGameModel> => {
            this.$log.debug('PlayModelBuilder:getModel getting game', id);
            return this.apiService.api.getGame({id: id}).$promise
                .then((game: IGameModel) => {
                    this.$log.debug('PlayModelBuilder:getModel received model', game);
                    return game;
                });
        };
    }

    class HomeController {

        static $inject = ['$log', '$state', '$scope', 'apiService'];
        constructor(
            private $log: ng.ILogService,
            private $state: ng.ui.IStateService,
            private $scope: ng.IScope,
            private apiService: IApiService
        ) {
            this.createGame();
        }

        private createGame = () => {
             // create a new game , redirect to 'play'
            this.apiService.api.createGame().$promise
                .then((game: IGameModel) => {
                    this.$log.debug('HomeController: createGame', game);
                    this.$state.go('play', {id: game.id})
                });
        }
    }

    class PlayController implements IPlayController{
        model: IGameModel;
        static $inject = ['$log', '$state', '$scope', 'apiService', 'game'];
        constructor(
            private $log: ng.ILogService,
            private $state: any,
            private $scope: IPlayScope,
            private apiService: IApiService,
            private game: IGameModel
        ) {
            $scope.vm = this;

            //Assign initial game model
            this.model = game;
        }

        openCell = (posx, posy) => {
            var updateRequest: IUpdateRequest = {
                method: 'open',
                x: posx,
                y: posy
            };
            this.$log.debug('PlayController:openCell ', updateRequest);
            this.apiService.api
                .updateGame(
                    {
                        id: this.$state.params.id
                    },
                    updateRequest
                )
                .then((game: IGameModel) => {
                    //update game
                    this.$log.debug('PlayController:openCell received game', game);
                    this.model = game;
                });
        };

        markCell = (posx, posy) => {
            var updateRequest: IUpdateRequest = {
                method: 'mark',
                x: posx,
                y: posy
            };
            this.$log.debug('PlayController:markCell ', updateRequest);
            this.apiService.api
                .updateGame(
                    {
                        id: this.$state.params.id
                    },
                    updateRequest
                )
                .then((game: IGameModel) => {
                    //update game
                    this.$log.debug('PlayController:markCell received game', game);
                    this.model = game;
                });
        };
    }

    angular.module('app')
        .controller('homeController', HomeController)
        .controller('playController', PlayController)
        .service('gameModelBuilder', GameModelBuilder);
}