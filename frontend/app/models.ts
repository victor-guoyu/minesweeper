/// <reference path="../../typings/tsd.d.ts" />

module app {
    export interface IModelBuilder<T> {
        getModel(): ng.IPromise<T>;
    }
}