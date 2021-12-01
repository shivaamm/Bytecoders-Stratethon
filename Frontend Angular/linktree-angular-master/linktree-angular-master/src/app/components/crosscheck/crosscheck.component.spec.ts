import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CrosscheckComponent } from './crosscheck.component';

describe('CrosscheckComponent', () => {
  let component: CrosscheckComponent;
  let fixture: ComponentFixture<CrosscheckComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CrosscheckComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CrosscheckComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
