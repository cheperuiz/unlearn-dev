package app;

import java.util.List;
import java.util.Optional;

import burgers.Burger;
import burgers.CheeseBurger;
import order.Order;

public class AppOrder {

	public static void main(String[] args) {
		
		Order order= new Order(529,2);
		order.getListBurguers().add(new Burger());
		order.getListBurguers().add(new CheeseBurger());
		
		order.setListBurguers(null);
		
		Optional<List<Burger>> burgerOpt= Optional.ofNullable(order.getListBurguers());
		
		/*
		if(order.getListBurguers()!= null && !order.getListBurguers().isEmpty()) {
			
		}
		
		if(burgerOpt.isPresent()) {
			System.out.println("there ara Burgers!!!!!!");
			order.getListBurguers().forEach(b->{
				b.makeRecipe();
			});
		}
		*/
	
		burgerOpt.ifPresent(listB->listB.forEach(b->b.makeRecipe()));
		
		
		
	}

}
