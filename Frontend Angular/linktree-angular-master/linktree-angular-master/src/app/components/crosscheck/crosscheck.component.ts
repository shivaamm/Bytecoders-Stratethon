import { Component, OnInit } from '@angular/core';
import { Router , ActivatedRoute } from "@angular/router";
import { AppService } from "../../app.service";
import {Location} from '@angular/common';
@Component({
  selector: 'app-crosscheck',
  templateUrl: './crosscheck.component.html',
  styleUrls: ['./crosscheck.component.css']
})

export class CrosscheckComponent implements OnInit {
  username:any;
  results:any;
  user:any;
  constructor(private rt:Router , private router : ActivatedRoute, private service : AppService,private _location: Location) { }

  ngOnInit() {
    this.service.getadministrator().subscribe(res=>{
      this.results = res;
      console.log(res);
    })
  }
  getLinkInfo(user){
    this.user = user;
  }
  deleteLink(){
    this.service.updatemaincount(this.user).subscribe(res=>{
      window.location.reload();
    })
  }
  deleteLinkdec(){
    this.service.updatemaincountdec(this.user).subscribe(res=>{
      window.location.reload();
    })
  }
}
