package order;

import java.util.ArrayList;
import java.util.List;

import burgers.Burger;

public class Order {
	
	private Integer numberOrder;
	private List<Burger> listBurguers;
	
	public Order(int numberOrder, int size) {
		this.numberOrder=numberOrder;
		this.listBurguers= new ArrayList<Burger>(size);
	}

	public Integer getNumberOrder() {
		return numberOrder;
	}

	public List<Burger> getListBurguers() {
		return listBurguers;
	}

	public void setListBurguers(List<Burger> listBurguers) {
		this.listBurguers = listBurguers;
	}
	
	
	

}
