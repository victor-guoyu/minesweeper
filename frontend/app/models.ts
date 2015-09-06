/// <reference path="../../typings/tsd.d.ts" />

module app {

    import IResource = ng.resource.IResource;

    export interface IModelBuilder<T> {
        getModel(id: string): ng.IPromise<T>;
    }

    export interface IPlayController {
        model: IGameModel;
        clickHandler(cell: ICell, action: string): void;
        newGame(): void;
    }

    export interface IPlayScope extends ng.IScope {
        vm: IPlayController
    }

    export interface ICell {
        revealed: boolean;
        marked: boolean;
        state: boolean;
        x: number;
        y:number;
        value: number;
    }

    export interface IGameModel {
        id: string;
        win: boolean;
        used_flag?: number; // This field is calculated at client side
        game_status: boolean;
        board: ICell[][];
        // The value is undefined if the user hasn't open anything yet
        last_open_x?: number;
        last_open_y?: number;
    }

    export interface IUpdateRequest {
        method: string;
        x: number;
        y: number;
    }

    export interface IGameResource extends ng.resource.IResourceClass<IResource<any>>{
        createGame(): IResource<IGameModel>; // create new game
        getGame(id:string): IResource<IGameModel>; // get game by id
        updateGame(id:string): IResource<IGameModel>;
    }

    export interface IApiService {
        api: any
    }

}