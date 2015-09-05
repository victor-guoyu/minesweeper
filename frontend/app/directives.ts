/// <reference path="../../typings/tsd.d.ts" />

(():void => {
    'use strict';

    angular.module('app').directive('ngRightClick', ['$parse', ($parse) => {
        return (scope, element, attrs) => {
            var fn = $parse(attrs.ngRightClick);
            element.bind('contextmenu', (event) => {
                scope.$apply(function () {
                    event.preventDefault();
                    fn(scope, {$event: event});
                });
            });
        };
    }]);
})();