import { Component, NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { showsComponent } from './shows.component';
import { WebService } from './web.service';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './home.component';
import { showComponent } from './show.component';
import { ReactiveFormsModule } from '@angular/forms';
import { AuthModule } from '@auth0/auth0-angular';
import { NavComponent } from './nav.component';
import { Ng2SearchPipeModule } from 'ng2-search-filter';
import { NgxPaginationModule } from 'ngx-pagination';
import { addmediaComponent } from './addmedia.component';
import { movieComponent } from './movie.component';
import { tvComponent } from './tv.component';


var routes : any = [
  {
    path:'',
    component: HomeComponent
  },
  {
    path:'shows',
    component: showsComponent
  },
  {
    path:'shows/:id',
    component: showComponent
  },
  {
    path:'Add',
    component: addmediaComponent
  },
  {  path: 'movies',
    component: movieComponent
  },
  {
    path: 'TvShows',
    component: tvComponent

  }  
];

@NgModule({
  declarations: [
    AppComponent, showsComponent, HomeComponent, showComponent, NavComponent,
    addmediaComponent, movieComponent, tvComponent
  ],
  imports: [
    BrowserModule, HttpClientModule,
    RouterModule.forRoot(routes), 
    ReactiveFormsModule,
    AuthModule.forRoot( {
      domain:'dev-y0vrvkpw.us.auth0.com',
      clientId:'PjDmKgGoQWh6eVbqBECVZA2XcZih8i5m',
      redirect_uri: `http://localhost:4200`
    }),
    Ng2SearchPipeModule,
    NgxPaginationModule

  ],
  providers: [WebService],
  bootstrap: [AppComponent]
})
export class AppModule { }
