import { Component } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';





@Component({
  selector: 'home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  constructor(private route: ActivatedRoute){}
}