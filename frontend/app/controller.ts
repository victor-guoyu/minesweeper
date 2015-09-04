/// <reference path="../../typings/tsd.d.ts" />
/// <reference path="./models.ts" />

module app.controllers {
    export interface IHomeController {
        model: IHomeModel;
    }

    export interface IHomeScope extends ng.IScope {
        vm: IHomeController;
    }

    export interface IHomeModel {

    }

    class HomeModelBuilder implements IModelBuilder<IHomeModel> {

        static $inject = ['$log'];
        constructor(
            private $log: ng.ILogService
        ) {

        }

        getModel = ():ng.IPromise<IHomeModel> => {
            return null;
        };

        private build = () => {

        };
    }

    class HomeController implements IHomeController{
        model: IHomeModel;
        static $inject = ['$log', '$scope', 'homeModel'];
        constructor(
            private $log: ng.ILogService,
            private $scope: IHomeScope,
            private homeModel: IHomeModel
        ) {
            $scope.vm = this;
            this.model = homeModel;
        }
    }

    angular.module('app')
        .controller('homeController', HomeController)
        .service('homeModelBuilder', HomeModelBuilder);
}